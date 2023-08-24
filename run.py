import os
import csv
import numpy as np
import argparse
from itertools import combinations
from inter_annotate import cohen_kappa_score,cohen_kappa,fleiss_kappa
from retrieve_annotations import load_class_names,create_track_groups,write_files,load_protobuf_dir,retrieve_annotator_classifications
from visualization import plot_confusion_matrix
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
    unique_keys,true_pairs,true_phases,IAA,FLEISS_IAA, cm = retrieve_annotator_classifications(class_names,annotations)

    # Write inter-agreement annotations to output file
    output_dir_cohen = 'results/IAA_cohen' if params["results_cohen"] is None else str(params["results_cohen"])
    output_fn_cohen = os.path.join(output_dir_cohen + '.csv')
    output_dir_fleiss = 'results/IAA_fleiss' if params["results_fleiss"] is None else str(params["results_fleiss"])
    output_fn_fleiss = os.path.join(output_dir_fleiss + '.csv')

    header = ['Video name','User Pair','']
    true_phases.append('overall')
    for phase in true_phases:
        header.append(phase)
    # header.append('Total Cohen IAA')
    
    rows = list()
    for annotator_pair in true_pairs:
        for video in unique_keys:
            row = dict()
            valid_row = False
            # Set header labels
            row['Video name'] = video
            first_annotator = annotator_pair[0]
            second_annotator = annotator_pair[1]
            row['User Pair'] = first_annotator+','+second_annotator
            row[''] = ''

            for phase in true_phases:
                if first_annotator+'_'+second_annotator in IAA[video].keys():
                    valid_row = True
                    if phase in IAA[video][first_annotator+'_'+second_annotator].keys():
                        row[phase] = IAA[video][first_annotator+'_'+second_annotator][phase]
                    else:
                        row[phase] = 0
            if valid_row is True:
                rows.append(row)
            
    with open(output_fn_cohen,'w') as f:
        writer = csv.DictWriter(f,fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)

    group_cm = dict()
    # group_names = ['Resident', 'Layperson']
    group_names = ['AMT_Turker']
    for group in group_names:
        group_cm[group] = np.zeros((len(true_phases[:-1]) + 1,len(true_phases[:-1]) + 1))

    for video in cm.keys():
        for pair in cm[video].keys():
            annotator_name = pair[1]
            group_name = [x for x in group_names if x in annotator_name]
            if len(group_name) > 0:
                group_name = group_name[0]
            else:
                group_name = 'AMT_Turker'

            group_cm[group_name] += cm[video][pair]

    for group in group_names:
        axis_labels = ['None']
        axis_labels.extend(true_phases[:-1])
        plot_confusion_matrix(group_cm[group], axis_labels,
                              normalize='Recall',
                              title='   ',
                              res_dir='./results_plot/cm/',
                              res_filename = 'Confusion_Matrix_'+group)
