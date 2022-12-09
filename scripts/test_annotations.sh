# Change to Data folder
data=../data
# Change to Output folder
outputs=../output_protobufs
# Change to source file
source=../run.py
# Change to output file
results_cohen=../results/IAA_cohen
results_fleiss=../results/IAA_fleiss

python ${source} --dataset-folder ${data} --output ${outputs} --results_cohen ${results_cohen} --results_fleiss ${results_fleiss}

