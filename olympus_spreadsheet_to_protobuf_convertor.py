import argparse
import csv
import glob
import os
import uuid

import google
import numpy as np
import datetime

from data_interface import sages_pb2
import google.protobuf.timestamp_pb2

# python ./action_triplet_convert.py --dataset-folder DATADIR OUTDIR

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
        print(filename)
        
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

                        if (row[i_column].replace(' ', '') not in invalid_symbols and row[i_column+1].replace(' ', '') not in invalid_symbols) and 'start' in row_name[i_column]:
                            row_label = row_name[i_column].split(' start')[0].split(' end')[0] 
                            
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
                                type=label, temporal_interval=protobuf_interval, video_id=video_id, annotator_id='jeckhoff'
                            )
                            new_entity = sages_pb2.SurgeryEntity(event=new_event, entity_id=new_id)

                            surgical_entities.append(new_entity)
                            interval_start_id = row_id
                        elif row[i_column].replace(' ', '') not in invalid_symbols and row[i_column+1].replace(' ', '') in invalid_symbols and 'start' in row_name[i_column]:
                            print(video_filename)
                            print(row_name[i_column].split(' start')[0].split(' end')[0] + "     start:" + row[i_column] + "    end:" +   row[i_column+1])

                    #sort according to starting time before adding to track
                    surgical_entities.sort(key=lambda x:x.event.temporal_interval.start.ToSeconds())
                    track = sages_pb2.Track(name=track_type, entities=surgical_entities)
                    tg = sages_pb2.TracksGroup(name=track_type + "_group", tracks=[track])

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
                    if 'start' in column or 'end' in column:
                        anno_name = column.split('.')[-1].split(' start')[0].split(' end')[0].replace(' ', '')
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



if __name__ == "__main__":
    args = parse_args()
    params = vars(args)
    annotation_set_dicts = {}
    dataset_folder = params["dataset_folder"]
    class_names = load_class_names(dataset_folder)
    for track_name in class_names.keys():
        track_dicts = create_track_groups(track_type=track_name,
                                          folder=dataset_folder,
                                          class_names = class_names[track_name],
                                          label_type='label_name')

        for key in track_dicts:
            if key not in annotation_set_dicts:
                annotation_set_dicts[key] = []
            annotation_set_dicts[key].append(track_dicts[key])


    for key in annotation_set_dicts:
        annotation_set = sages_pb2.AnnotationSet(tracks_groups=annotation_set_dicts[key])
        folder_name = os.path.expandvars(os.path.expanduser(params['output']))
        os.makedirs(folder_name, exist_ok=True)

        output_pathname = os.path.join(folder_name,key + '.pb')
        with open(output_pathname,'wb') as fp:
            fp.write(annotation_set.SerializeToString())
            fp.close()
    