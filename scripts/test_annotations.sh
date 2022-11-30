# Change to Data folder
data=~/Downloads/inter_annotation/data
# Change to Output folder
outputs=~/Downloads/inter_annotation/output_protobufs
# Change to source file
source=~/Downloads/inter_annotation/run.py
# Change to output file
results_cohen=~/Downloads/inter_annotation/results/IAA_cohen
results_fleiss=~/Downloads/inter_annotation/results/IAA_fleiss

python ${source} --dataset-folder ${data} --output ${outputs} --results_cohen ${results_cohen} --results_fleiss ${results_fleiss}

