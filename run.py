import os
import argparse
from itertools import combinations
from inter_annotate import cohen_kappa_score
from csv_to_protobuf import load_class_names,create_track_groups,write_files,load_protobuf_dir,retrieve_annotator_classifications

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
    class_names,annotations = load_protobuf_dir('output_protobufs')
    num_classes = len(class_names['phase'])+1

    # Retrieve annotations with classifications with fps=1 and combinations of annotator pairs
    unique_keys,unique_annotators,A = retrieve_annotator_classifications(class_names,annotations)
    Z = list(combinations(range(len(unique_annotators)),2))

    # Write inter-agreement annotations to output file
    output_dir = 'results/IAA'
    output_fn = os.path.join(output_dir + '.txt')
    with open(output_fn,'w') as fp:
        for pair in Z:
            avg_scores = 0
            for video in unique_keys:
                first = A[video][pair[0]]
                second = A[video][pair[1]]
                avg_scores += cohen_kappa_score(first,second,num_classes)
            avg_scores /= len(unique_keys)
            annotate_text = 'First annotator: ' + unique_annotators[pair[0]] + '; Second annotator: ' + \
                unique_annotators[pair[1]] + '\n--> Avg scores: ' + str(avg_scores.item()) + '\n'
            fp.write(annotate_text)
            fp.write('\n')
    fp.close()
