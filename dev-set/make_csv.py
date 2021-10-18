import json 
import pdb 


PATH_TO_K_MEANS = "k_means_dev_set_filtered_latest_new.json"

with open(PATH_TO_K_MEANS, "r") as json_in: 
     json_with_clusters = json.load(json_in)


with open("../data-cleaning/all_references.json", "r") as json_in: 
     data = json.load(json_in) 

with open("../../tacl/data/references_for_lm.json", "r") as json_in: 
     all_data = json.load(json_in)

# dict_keys(['clusters', 'centroids', 'centroids_by_prob', 'Centroids_with_revised', 'SelectedCentroids', 'GPT+Finetuning+P-perplexityPred',
# 'GPT+Finetuning+P-perplexityCorr', 'GPT+FinetuningCorrect', 'CorrectReference', 'LeftContext', 'GPTPred', 'GPTCorrect', 'key', 'GPT+FinetuningPred', 'RevisedSentence', 'revised_untill_insertion', 'revised_after_insertion', 'reference-type', 'par', 'language_model_text', 'index_of_reference', 'filtered_fillers'])

def main(): 
    for key, _ in json_with_clusters.items(): 
        print(data[key]['Filename']+".bz2") 
        pdb.set_trace()

main()