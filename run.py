import os
import csv
import numpy as np
import argparse
from itertools import combinations
from inter_annotate import cohen_kappa_score,cohen_kappa,fleiss_kappa
from retrieve_annotations import load_class_names,create_track_groups,write_files,load_protobuf_dir,retrieve_annotator_classifications

def parse_args(): 
    """Parse arguments

    Returns:
        params: arguments object
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=str, help="The output filename")
    parser.add_argument("--dataset-folder", type=str, default=None, help="The location of the dataset files")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose flag")
    parser.add_argument("--results_cohen", type=str, default=None, help="Final IAA Cohen results file")
    parser.add_argument("--results_fleiss", type=str, default=None, help="Final IAA Fleiss results file")
    params = parser.parse_args()
    return params

if __name__ == "__main__":
    args = parse_args()
    params = vars(args)
    annotation_set_dicts = {}
    dataset_folder = params["dataset_folder"]
    class_names = load_class_names(dataset_folder)
    for track_name in class_names:
        track_dicts = create_track_groups(track_type=track_name,
                                          folder=dataset_folder,
                                          class_names = class_names,
                                          label_type='label_name')
        for key in track_dicts:
            if key not in annotation_set_dicts:
                annotation_set_dicts[key] = []
            annotation_set_dicts[key].append(track_dicts[key])

    # Write protobuf files
    write_files(annotation_set_dicts,params)

    # Load and read protobuf files
    class_names,annotations = load_protobuf_dir(params["output"])

    # Retrieve the annotations
    unique_keys,true_pairs,true_phases,IAA,FLEISS_IAA = retrieve_annotator_classifications(class_names,annotations)

    # Write inter-agreement annotations to output file
    output_dir_cohen = 'results/IAA_cohen' if params["results_cohen"] is None else str(params["results_cohen"])
    output_fn_cohen = os.path.join(output_dir_cohen + '.csv')
    output_dir_fleiss = 'results/IAA_fleiss' if params["results_fleiss"] is None else str(params["results_fleiss"])
    output_fn_fleiss = os.path.join(output_dir_fleiss + '.csv')

    header = ['Video name','User Pair','']
    for phase in true_phases:
        header.append(phase)
    # header.append('Total Cohen IAA')
    
    rows = list()
    for video in unique_keys:
        for annotator_pair in true_pairs:
            row = dict()

            # Set header labels
            row['Video name'] = video
            first_annotator = annotator_pair[0]
            second_annotator = annotator_pair[1]
            row['User Pair'] = first_annotator+','+second_annotator
            row[''] = ''

            total_first_annotation_video = list()
            total_second_annotation_video = list()
            for phase_idx,phase in enumerate(true_phases):
                phase_idx = phase_idx + 1 
                if IAA[video][first_annotator+'_'+second_annotator][phase_idx]:     # list not empty
                    first_annotation_arr = IAA[video][first_annotator+'_'+second_annotator][phase_idx][0]
                    second_annotation_arr = IAA[video][first_annotator+'_'+second_annotator][phase_idx][1]
                    if len(first_annotation_arr)!=0:
                        score = cohen_kappa(first_annotation_arr,second_annotation_arr)
                        row[phase] = score
                    else:
                        row[phase] = 0

                    total_first_annotation_video += first_annotation_arr
                    total_second_annotation_video += second_annotation_arr
            total_score = cohen_kappa(total_first_annotation_video,total_second_annotation_video)
            # row['Total Cohen IAA'] = total_score
            rows.append(row)

    '''
    # Compute Total Averages
    avg_row = list()
    for annotator_pair in true_pairs:
        row['Video name'] = 'Average'
        first_annotator = annotator_pair[0]
        second_annotator = annotator_pair[1]
        row['User Pair'] = first_annotator+','+second_annotator
        row[''] = ''
        for video in unique_keys():
            for phase in true_phases:
    '''

    with open(output_fn_cohen,'w') as f:
        writer = csv.DictWriter(f,fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

    '''
    header = ['Video name','User Group','']
    for phase in true_phases:
        header.append(phase)
    header.append('Total Cohen IAA')
    
    rows = list()
    for video in unique_keys:
        M = FLEISS_IAA[video]
        M = np.array(M)
        print(M[:,1:].shape)
        score = fleiss_kappa(M[:,1:])
        score2 = fleiss_kappa(M)
        print('Score 1: ',score,' Score 2: ',score2)
    with open(output_fn_fleiss,'w') as f:
        writer = csv.DictWriter(f,fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)
    '''
