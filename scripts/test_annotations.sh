# Change to Data folder
# data=../data/surgical_endoscopy
data=../data/AMT/
# Change to Output folder
# outputs=../output_protobufs/layperson_resident/
outputs=../output_protobufs/amt/
# Change to source file
source=../run.py
# Change to output file
# results_cohen=../results/IAA_cohen_master
# results_fleiss=../results/IAA_fleiss_master
results_cohen=../results/IAA_cohen_amt
results_fleiss=../results/IAA_fleiss_amt

python ${source} --dataset-folder ${data} --output ${outputs} --results_cohen ${results_cohen} --results_fleiss ${results_fleiss}

