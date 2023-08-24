import sys
import math
import argparse
import csv
import glob
import os
import uuid
import google
import numpy as np
import datetime
import sages_pb2
from sages_pb2 import *
import multidict
import google.protobuf.timestamp_pb2
from inter_annotate import cohen_kappa_score, cohen_kappa, jaccard_index, confusion_matrix
from itertools import combinations,permutations

def seconds_to_timestamp(seconds):
    """Convert seconds to a protobuf timestamp.

    Args:
        seconds (float): seconds timespan

    Returns:
        timestamp: google.protobuf.timestamp_pb2.Timestamp
    """
    timestamp = google.protobuf.timestamp_pb2.Timestamp()
    timestamp.seconds = np.compat.long(seconds) // 1
    timestamp.nanos = np.compat.long((seconds - timestamp.seconds) * 1e9)
    return timestamp


def isLast(itr):
    """wraps an iterator and returns whether we're at the last element.
    https://stackoverflow.com/questions/970983/have-csv-reader-tell-when-it-is-on-the-last-line
    """
    old = itr.__next__()
    for new in itr:
        yield False, old
        old = new
    yield True, old


def create_track_groups(track_type, folder, class_names, label_type):
    """read a folder with txt files from camma annotation, convert to protobuf annotation track group

    Args:
        track_type (str): The track type / name.
        folder (str): The folder where the txt files are.
        label_type (str): Either label_name or binary_labels

    Returns:
        dict: mapping from surgery id to a track group for that surgery.
    """
    assert(label_type in ['label_name','binary_labels'])
    results_dict = {}
    folder_name = os.path.expandvars(os.path.expanduser(folder))
    txt_files = sorted(glob.glob(os.path.join(folder_name, "*.csv")))
    labels_set = set()
    labels_list = list()
    invalid_symbols = ['N/A', 'NA', '']
    for filename in txt_files:
        # if params["verbose"]:
            # print("annotation filename: {}".format(filename))
        with open(filename, "r") as fp:
            csvreader = csv.reader(fp, delimiter=",")
            segments_status={}
            last_label = None
            interval_start_id = 1
            intervals = []
            class_count = dict()
            for i_row, (is_last,row) in enumerate(isLast(csvreader)):
                surgical_entities = []
                annotator_name = row[1].replace(' ','')
                if i_row == 0:
                    continue

                if i_row == 1:
                    row_name = []
                    for idx_column in range(len(row)-1):
                        row_name_tmp = row[idx_column].split('. ')[-1]
                        row_name.append(row_name_tmp)

                else:

                    for i_column in range(2, len(row)-1):
                        row_id = i_row
                        video_filename = row[0].replace(' ', '')
                        video_id= video_filename

                        if video_filename == '':
                            continue

                        if (row[i_column].replace(' ', '') not in invalid_symbols and row[i_column+1].replace(' ', '') not in invalid_symbols) and 'Start' in row_name[i_column]:
                            row_label = row_name[i_column].split(' Start')[0].split(' End')[0].strip()
                            start_time = (datetime.datetime.strptime(row[i_column].replace(' ', ''), "%H:%M:%S") - datetime.datetime(1900, 1, 1)).total_seconds()
                            end_time = (datetime.datetime.strptime(row[i_column+1].replace(' ', ''), "%H:%M:%S") - datetime.datetime(1900, 1, 1)).total_seconds()
                            label = row_label
                            labels_set.add(row_label)

                            # save interval
                            new_interval_info = {
                                "start_time": start_time,
                                "end_time": end_time,
                                "label": label,
                            }
                            if end_time < start_time:
                                continue
                            elif end_time - start_time > 2400:
                                print('long phases:')
                                print(video_filename)
                                print(new_interval_info) 

                            if label in class_count:
                                class_count[label] += end_time - start_time
                            else:
                                class_count[label] = 0

                            intervals.append(new_interval_info)
                            last_label = row_label
                            # print(new_interval_info)
                            new_id = str(uuid.uuid4())
                            protobuf_start_time = seconds_to_timestamp(start_time)
                            protobuf_end_time = seconds_to_timestamp(end_time)
                            protobuf_interval = sages_pb2.TemporalInterval(
                                start=protobuf_start_time, end=protobuf_end_time, start_exact=True, end_exact=True
                            )
                            new_event = sages_pb2.Event(
                                type=label, temporal_interval=protobuf_interval, video_id=video_id, annotator_id=annotator_name
                            )
                            new_entity = sages_pb2.SurgeryEntity(event=new_event, entity_id=new_id)

                            surgical_entities.append(new_entity)
                            interval_start_id = row_id
                        elif row[i_column].replace(' ', '') not in invalid_symbols and row[i_column+1].replace(' ', '') in invalid_symbols and 'Start' in row_name[i_column]:
                            print(video_filename)
                            print(row_name[i_column].split(' Start')[0].split(' End')[0] + "     Start:" + row[i_column] + "    End:" +   row[i_column+1])

                    #sort according to starting time before adding to track
                    surgical_entities.sort(key=lambda x:x.event.temporal_interval.start.ToSeconds())
                    track = sages_pb2.Track(name=track_type, entities=surgical_entities)
                    tg = sages_pb2.TracksGroup(name=track_type + "_group", tracks=[track])

                    video_filename_full = video_filename+'_'+annotator_name if annotator_name != '' else video_filename
                    if video_filename_full == '':
                        continue
                    results_dict[video_filename_full] = tg

    # print(str(labels_set))
    # print(len(str(labels_set).split(',')))
    # print(class_count)
    return results_dict


def load_csv(filename=None):
    anno = dict()
    with open(filename) as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',', quotechar='|')
        video_name = os.path.splitext(next(csv_data)[0])[0]
        for i_row, row in enumerate(csv_data):
            if i_row == 0:
                for i_column, column in enumerate(row[2:]):
                    if 'Start' in column or 'End' in column:
                        anno_name = column.split('.')[-1].split(' Start')[0].split(' End')[0].replace(' ', '').strip()
                        anno_label = 1.0
                        anno[anno_name] = anno_label
    return anno

def load_class_names(dataset_folder = None):
    class_names = dict()
    folder_name = os.path.expandvars(os.path.expanduser(dataset_folder))
    csv_files = glob.glob(os.path.join(folder_name, "*.csv"))
    #  print(f"load_class_names: Found {len(csv_files)} spreadsheet files in {dataset_folder}.")

    csv_anno = dict()
    for filename in csv_files:
        video_name = os.path.split(filename)[-1].split('.')[0].split('_')[0]
        frame_num = os.path.split(filename)[-1].split('.')[0].split('_')[1]
        if video_name not in csv_anno.keys():
            csv_anno[video_name] = []
        anno = load_csv(filename=filename)

        track_name = 'phase' # to be consistent with the anvil annotation outputs
        class_names[track_name] = []

        for class_name in anno.keys():
            class_names[track_name].append(class_name)
    return class_names


def load_protobuf_dir(
    annotation_dir,
    missing_annotations_is_okay=False,
    prefix="",
    verbose=True,
    phase_translation_file=None,
    allowed_track_names=None,
):
    """
    load annotation information from protobuf dataset
    :param annotation_dir: a folder contains .pb files
    :param missing_annotations_is_okay:
    :param prefix: prefix string if any
    :param verbose:
    :param phase_translation_file: the phase translation filename
    :param allowed_track_names: the track names that will actually be read. Use None to allow all tracks.
    :return:
    """
    steps = {}
    annotations = {}

    files_list = sorted(glob.glob(os.path.join(annotation_dir, "*.pb")))
    if phase_translation_file is not None:
        from data_interface.base_utils import read_phase_mapping

        phase_name_map = read_phase_mapping(phase_translation_file)
    else:
        phase_name_map = {}

    for filename in files_list:
        try:
            tracks = load_protobuf_file(filename)
        except:
            print("Error in " + filename)
            raise

        video_file = os.path.split(filename)[-1].split(".")[0]
        annotations[os.path.join(prefix, video_file)] = multidict.MultiDict()
        total_time = 0
        pre_phase_name = ""
        for trk in tracks:
            if trk["track_name"] == "point" or trk["track_name"] == "other steps":
                continue
            track_name = trk["track_name"]
            if allowed_track_names is not None and track_name not in allowed_track_names:
                continue

            props = trk["entity"].event
            name = props.type
            if name in phase_name_map.keys():
                name = phase_name_map[name]

            start = float(str(props.temporal_interval.start.seconds) + "." + str(props.temporal_interval.start.nanos))
            end = float(str(props.temporal_interval.end.seconds) + "." + str(props.temporal_interval.end.nanos))
            temporal_attr = "interval"
            if start == 0 and end == 0:
                temporal_attr = "point"
                start = float(str(props.temporal_point.point.seconds) + "." + str(props.temporal_point.point.nanos))
                end = start
            video_id = props.video_id
            annotator_id = props.annotator_id
            if name is None:
                if verbose:
                    print("Attribute name is missing, " + filename)
                continue
            if track_name not in steps:
                steps[track_name] = set()
            steps[track_name].add(name)
            annotations[os.path.join(prefix, video_file)].add(
                name,
                {
                    "start": start,
                    "end": end,
                    "temporal_attr": temporal_attr,
                    "annotator_id": annotator_id,
                    "track_name": track_name,
                    "video_id": video_id,
                },
            )
            total_time += float(end) - float(start)
            if track_name == "major operative phases":
                pre_phase_name = name
    if len(annotations) == 0 and not missing_annotations_is_okay:
        print("Missing annotations: " + annotation_dir)
        raise MissingAnnotationsError(annotation_dir)
    # sort the class_name in alphabet order, otherwise each training has different class names
    class_names = {}
    for key in steps:
        class_names[key] = list(steps[key])
        class_names[key].sort()
    return class_names, annotations


def load_protobuf_file(filename):
    with open(filename, "rb") as fp:
        annotation_set = AnnotationSet()
        annotation_set.ParseFromString(fp.read())
        all_entities = []
        for tracks_group in annotation_set.tracks_groups:
            for tr in tracks_group.tracks:
                for entity in tr.entities:
                    all_entities.append({"track_name": tr.name, "entity": entity})
    return all_entities

def write_files(annotation_set_dicts,params):
    for key in annotation_set_dicts:
        annotation_set = sages_pb2.AnnotationSet(tracks_groups=annotation_set_dicts[key])
        folder_name = os.path.expandvars(os.path.expanduser(params['output']))
        os.makedirs(folder_name, exist_ok=True)
        output_pathname = os.path.join(folder_name,key + '.pb')
        with open(output_pathname,'wb') as fp:
            fp.write(annotation_set.SerializeToString())
            fp.close()

def retrieve_true_values(class_names,unique_annotators):
    #### Merge phase segments belonging to the same phase into one; In other words, we remove all digits from phase titles except if
    #### the phase is a Checkpoint
    true_phases = list()
    for phase in class_names['phase']:
        phase = phase if 'Checkpoint' in phase else (''.join(i for i in phase if not i.isdigit()))
        if phase not in true_phases:
            true_phases.append(phase)
    true_phases = ['Port Placement', 'Fundus Retraction', 'Release of Gallbladder Peritoneum', "Dissection of Calot's Triangle",
                   'Checkpoint 1',  'Clipping Cystic Artery', 'Clipping Cystic Duct', 
                   'Division Cystic Artery', 'Division Cystic Duct', 'Checkpoint 2',
                   'Removal of Gallbladder from Liver Bed', 'Bagging of Gallbladder']

    ##### Ground truth annotator: Medical resident, Compute annotation scores against other non-residents
    Z = list(combinations(unique_annotators,2))
    true_pairs = list()
    for pair in Z:
        if 'GroundTruth' in pair[0] or 'GroundTruth' in pair[1]:
            true_pairs.append(pair) if 'GroundTruth' in pair[0] else true_pairs.append((pair[1], pair[0]))

    true_pairs.sort()
    return true_phases,true_pairs

def retrieve_annotator_classifications(class_names,annotations):
    fps = 1.0
    all_keys = [key.split('_')[0] for key in annotations.keys()]
    
    all_annotators = [key.split('_')[1] for key in annotations.keys()]
    unique_keys = [*set(all_keys)]
    unique_annotators = [*set(all_annotators)]
    true_phases, true_pairs = retrieve_true_values(class_names,unique_annotators)
    annotators_for_video = dict()
    #### FIND maximum time stamp to define the length for each video
    max_vid_lens = dict()
    for video in unique_keys:
        annotators_for_video[video] = list()
        max_vid_len = 0
        for annotator in unique_annotators:
            for phase in class_names['phase']:
                if video+'_'+annotator in annotations.keys():
                    annotators_for_video[video].append(annotator)
                    if phase in annotations[video+'_'+annotator]:
                        max_vid_len = int(max(max_vid_len,((annotations[video+'_'+annotator])[phase])['end']))
        max_vid_lens[video] = max_vid_len+1

    annotations_true_phase = dict()
    for video in unique_keys:
        for annotator in annotators_for_video[video]:
            annotations_true_phase[video+'_'+annotator] = dict()

            for phase in class_names['phase']:
                if phase in annotations[video+'_'+annotator]:
                    true_phase = phase if 'Checkpoint' in phase else (''.join(i for i in phase if not i.isdigit())).strip()
                    if true_phase not in annotations_true_phase[video+'_'+annotator].keys():
                        annotations_true_phase[video+'_'+annotator][true_phase] = dict()
                        annotations_true_phase[video+'_'+annotator][true_phase]['start'] = annotations[video+'_'+annotator][phase]['start']
                        annotations_true_phase[video+'_'+annotator][true_phase]['end'] = annotations[video+'_'+annotator][phase]['end']
                    else:
                        prev_start = annotations_true_phase[video+'_'+annotator][true_phase]['start']
                        prev_end = annotations_true_phase[video+'_'+annotator][true_phase]['end']
                        
                        annotations_true_phase[video+'_'+annotator][true_phase]['start'] = min(annotations[video+'_'+annotator][phase]['start'],prev_start)
                        annotations_true_phase[video+'_'+annotator][true_phase]['end'] = max(annotations[video+'_'+annotator][phase]['end'],prev_end)


    
    A = dict()
    error_list = list()
    cm = dict()
    for video in unique_keys:
        A[video] = dict()
        for annotator_pair in true_pairs:
            first_annotator = annotator_pair[0]
            second_annotator = annotator_pair[1]
            if video+'_'+first_annotator in annotations_true_phase.keys() and video+'_'+second_annotator in annotations_true_phase.keys():
                ann_dict_first = annotations_true_phase[video+'_'+first_annotator]
                ann_dict_second = annotations_true_phase[video+'_'+second_annotator]
                A[video][first_annotator+'_'+second_annotator] = dict() 
                # for phase in class_names['phase']:
                for phase in true_phases:
                    if phase in ann_dict_first and phase in ann_dict_second:
                        start_first = math.floor(ann_dict_first[phase]['start'])
                        end_first = math.floor(ann_dict_first[phase]['end'])
                        start_second = math.floor(ann_dict_second[phase]['start'])
                        end_second = math.floor(ann_dict_second[phase]['end'])


                        MIN_START = min(start_first,start_second)
                        MAX_END = max(end_first,end_second)
                        phase_arr_first = np.zeros((MAX_END-MIN_START)+1)
                        phase_arr_second = np.zeros((MAX_END-MIN_START)+1)

                        for i in range(len(phase_arr_first)):
                            if start_first<=(i+MIN_START) and end_first>=(i+MIN_START):
                                phase_arr_first[i] = 1.
                            if start_second<=(i+MIN_START) and end_second>=(i+MIN_START):
                                phase_arr_second[i] = 1.
                        # Compute IAA Score 
                        score = jaccard_index(phase_arr_first,phase_arr_second)
                        # score = cohen_kappa_score(phase_arr_second,phase_arr_first,num_classes=2).item()*-1
                        
                        # print(start_first)
                        # print(end_first)
                        # print(start_second)
                        # print(end_second)
                        # print(score)
                        # if start_first == 0 or end_first == 0 or start_second == 0 or end_second == 0:
                        #     import ipdb; ipdb.set_trace()


                    elif phase in ann_dict_first or phase in ann_dict_second:
                        score = 0.0 # if phase is annotated in one annotator and not in the other
                    elif (phase not in ann_dict_first) and (phase not in ann_dict_second):
                        score = 1.0 # if phase is not annotated in either annotator

                    A[video][first_annotator+'_'+second_annotator][phase] = score
                
                # # overall cohen kappa per video 
                # phase_arr_first = np.zeros(max_vid_lens[video])
                # phase_arr_second = np.zeros(max_vid_lens[video])
                # for i in range(max_vid_lens[video]):
                #     for phase in true_phases:
                #         if phase in ann_dict_first.keys():
                #             if i > ann_dict_first[phase]['start'] and i < ann_dict_first[phase]['end']:
                #                 if phase_arr_first[i] == 0:
                #                     phase_arr_first[i] = true_phases.index(phase) + 1
                #                 else:
                #                     error_str = video + ' '+ first_annotator + ' '+ phase + ': ' + str(ann_dict_first[phase]['start']) + ':' + str(ann_dict_first[phase]['end'])
                #                     if error_str not in error_list:
                #                         error_list.append(error_str)
                #         if phase in ann_dict_second.keys():
                #             if i > ann_dict_second[phase]['start'] and i < ann_dict_second[phase]['end']:
                #                 if phase_arr_second[i] == 0:
                #                     phase_arr_second[i] = true_phases.index(phase) + 1
                #                 else:
                #                     error_str = video + ' '+ second_annotator + ' ' + phase + ': ' + str(ann_dict_second[phase]['start']) + ':' + str(ann_dict_second[phase]['end'])
                #                     if error_str not in error_list:
                #                         error_list.append(error_str)
                # score = cohen_kappa(phase_arr_first,phase_arr_second)


                # overall cohen kappa per video 
                phase_arr_first = np.zeros(max_vid_lens[video])
                phase_arr_second = np.zeros(max_vid_lens[video])
                for i in range(max_vid_lens[video]):
                    for phase in true_phases:
                        if phase in ann_dict_first.keys():
                            if i > ann_dict_first[phase]['start'] and i < ann_dict_first[phase]['end']:
                                if phase_arr_first[i] == 0:
                                    phase_arr_first[i] = true_phases.index(phase) + 1
                                else:
                                    error_str = video + ' '+ first_annotator + ' '+ phase + ': ' + str(ann_dict_first[phase]['start']) + ':' + str(ann_dict_first[phase]['end'])
                                    if error_str not in error_list:
                                        error_list.append(error_str)
                        for phase2 in ann_dict_second.keys():
                            if i > ann_dict_second[phase2]['start'] and i < ann_dict_second[phase2]['end']:
                                if phase_arr_second[i] == 0:
                                    phase_arr_second[i] = true_phases.index(phase2) + 1
                                elif phase_arr_second[i] != phase_arr_first[i]:
                                    phase_arr_second[i] = true_phases.index(phase2) + 1
                                else:
                                    error_str = video + ' '+ second_annotator + ' ' + phase2 + ': ' + str(ann_dict_second[phase2]['start']) + ':' + str(ann_dict_second[phase2]['end'])
                                    if error_str not in error_list:
                                        error_list.append(error_str)
                score = cohen_kappa(phase_arr_first,phase_arr_second)

                # overall cohen kappa per video for every annotation even the annotation overlaps with other annotations 
                # phase_arr_first = []
                # phase_arr_second = []
                # for phase in true_phases:
                #     if phase in ann_dict_first.keys():
                #         for i in range(math.floor(ann_dict_first[phase]['start']),math.floor(ann_dict_first[phase]['end'])):
                #             phase_arr_first.append(true_phases.index(phase) + 1)
                #             phase_t_second = 0
                #             for phase2 in ann_dict_second.keys():
                #                 if i > ann_dict_second[phase2]['start'] and i < ann_dict_second[phase2]['end']:
                #                         if phase_t_second != 0:
                #                             import ipdb; ipdb.set_trace()
                #                         phase_t_second =  true_phases.index(phase2) + 1
                #             phase_arr_second.append(phase_t_second)
                # phase_arr_first = np.array(phase_arr_first)
                # phase_arr_second = np.array(phase_arr_second)
                # score = cohen_kappa(phase_arr_first,phase_arr_second)
                if video not in cm.keys():
                    cm[video] = dict()

                cm[video][annotator_pair] = confusion_matrix(phase_arr_first,phase_arr_second, len(true_phases)+1)
                A[video][first_annotator+'_'+second_annotator]['overall'] = score
                # Compute IAA Score

    #### FLEISS SCORE: Compute for Medical Residents and Non-residents
    IAA = A

    FLEISS_IAA = dict()
    print('Phase may have contradictions within same annotator are:')
    for error in error_list:
        print(error)

    return unique_keys,true_pairs,true_phases,IAA,FLEISS_IAA, cm
