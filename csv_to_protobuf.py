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

def parse_args():
    """Parse arguments

    Returns:
        params: arguments object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, help="The output filename")
    parser.add_argument("--dataset-folder", type=str, default=None, help="The location of the dataset files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose flag")
    params = parser.parse_args()
    return params


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
        if params["verbose"]:
            print("annotation filename: {}".format(filename))
        with open(filename, "r") as fp:
            csvreader = csv.reader(fp, delimiter=",")
            segments_status={}
            last_label = None
            interval_start_id = 1
            intervals = []
            class_count = dict()
            for i_row, (is_last,row) in enumerate(isLast(csvreader)):
                surgical_entities = []
                if i_row == 0:
                    continue

                if i_row == 1:
                    row_name = []
                    for idx_column in range(len(row)-1):
                        row_name_tmp = row[idx_column].split('. ')[-1]
                        row_name.append(row_name_tmp)

                else:

                    for i_column in range(1, len(row)-1):
                        row_id = i_row
                        video_filename = row[0].replace(' ', '')
                        video_id= video_filename

                        if video_filename == '':
                            continue

                        if (row[i_column].replace(' ', '') not in invalid_symbols and row[i_column+1].replace(' ', '') not in invalid_symbols) and 'Start' in row_name[i_column]:
                            row_label = row_name[i_column].split(' Start')[0].split(' End')[0] 
                            
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
                                type=label, temporal_interval=protobuf_interval, video_id=video_id, annotator_id=row[0]+'_'+row[1]
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
                    print(video_filename)
                    results_dict[video_filename] = tg

    print(str(labels_set))
    print(len(str(labels_set).split(',')))
    print(class_count)
    return results_dict


def load_csv(filename=None):
    anno = dict()
    with open(filename) as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',', quotechar='|')
        video_name = os.path.splitext(next(csv_data)[0])[0]
        for i_row, row in enumerate(csv_data):
            if i_row == 0:
                for i_column, column in enumerate(row[3:]):
                    if 'Start' in column or 'End' in column:
                        anno_name = column.split('.')[-1].split(' Start')[0].split(' End')[0].replace(' ', '')
                        anno_label = 1.0
                        anno[anno_name] = anno_label
    return anno

def load_class_names(dataset_folder = None):
    class_names = dict()
    folder_name = os.path.expandvars(os.path.expanduser(dataset_folder))
    csv_files = glob.glob(os.path.join(folder_name, "*.csv"))
    print(f"load_class_names: Found {len(csv_files)} spreadsheet files in {dataset_folder}.")

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



if __name__ == "__main__":
    args = parse_args()
    params = vars(args)
    annotation_set_dicts = {}
    dataset_folder = params["dataset_folder"]
    class_names = load_class_names(dataset_folder)
    print(class_names.keys())
    for track_name in class_names.keys():
    # for track_name in class_names['phase']:
        track_dicts = create_track_groups(track_type=track_name,
                                          folder=dataset_folder,
                                          # class_names = class_names['phase'],
                                          class_names = class_names,
                                          label_type='label_name')
        for key in track_dicts:
            if key not in annotation_set_dicts:
                annotation_set_dicts[key] = []
            annotation_set_dicts[key].append(track_dicts[key])
    print(annotation_set_dicts)
 

    if False:
        for key in annotation_set_dicts:
            annotation_set = sages_pb2.AnnotationSet(tracks_groups=annotation_set_dicts[key])
            folder_name = os.path.expandvars(os.path.expanduser(params['output']))
            os.makedirs(folder_name, exist_ok=True)
            
            annotator_name = 'test'
            output_pathname = os.path.join(folder_name,key + '_{}.pb'.format(annotator_name))
            with open(output_pathname,'wb') as fp:
                fp.write(annotation_set.SerializeToString())
                fp.close()

    if False:
        # Reading from pb files
        # print(load_protobuf_file('outputs/LC39.pb'))
        class_names,annotations = load_protobuf_dir('outputs')
        print('Class Names',class_names)
        print('Annotation',annotations.keys())
        print('\n',annotations['LC39'],'\n')
        print('\n',annotations['LC147'],'\n')
        print('\n',annotations['LC185'],'\n')
