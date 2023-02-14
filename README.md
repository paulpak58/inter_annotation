# Inter-Annotator Agreement for Surgical Annotations
Each surgical video is annotated by different annotators. We first load this information from an input spreadsheet and then calculate the inter-annotator agreement per frame. The Jaccard Index is computed between each pair of annotators, and the Multi-class Cohen Kappa Score is computed for the overall video.

## Setup
> conda env create -n inter_annotator --file inter_annotator.yml

> conda activate inter_annotator


## Structure
`retrieve_annotations.py` contains methods to change file structure and the one that constructs the final matrix of annotations  
`inter_annotate.py` contains methods to compute the various scores  
`sages_pb2.py` contains helpers for dealing with protobuf files, which are used as intermediates before the final matrix is created  
`visualization.py` contains code to visualize confusion matrices  
`run.py` contains the main driver  


## Running Script
You can change any of the file directories as needed. Note that we decided not to calculate the Fleiss score and instead used the Jaccard Index and Cohen Kappa Score but may consider it in the future, which is why the flag for a Fleiss output file still exists.
> cd scripts

> sh test_annotations.sh