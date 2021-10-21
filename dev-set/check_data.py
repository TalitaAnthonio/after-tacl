import json 
import pdb 
from tools import * 


PATH_TO_MAIN = "../get-context/filtered_set_dev_articles_tokenized_context_latest_with_context.json"
PATH_TO_CLUSTERS = "../dev-set/k_means_dev_set_filtered_latest_new.json"
BATCH_NR = 5
filename_to_write = "implicit_references_batch{0}_dev.csv".format(BATCH_NR)

with open(PATH_TO_MAIN, "r") as json_in: 
     data_with_context = json.load(json_in)

with open(PATH_TO_CLUSTERS, "r") as json_in: 
     clusters = json.load(json_in)


# dict_keys(['clusters', 'centroids', 'centroids_by_prob', 'Centroids_with_revised', 'SelectedCentroids', 'GPT+Finetuning+P-perplexityPred', 'GPT+Finetuning+P-perplexityCorr', 'GPT+FinetuningCorrect', 'CorrectReference', 'LeftContext', 'GPTPred', 'GPTCorrect', 'key', 'GPT+FinetuningPred', 'RevisedSentence', 'revised_untill_insertion', 'revised_after_insertion', 'reference-type', 'par', 'language_model_text', 'index_of_reference', 'filtered_fillers'])

def main(): 
    counter = 0 
    for key, _ in data_with_context.items(): 
        print("================================")
        if len(clusters[key]["Centroids_with_revised"]) == 5: 
            #pdb.set_trace()
            counter +=1 
            print(clusters[key]["Centroids_with_revised"], len(clusters[key]["Centroids_with_revised"])) 
            print(clusters[key]["SelectedCentroids"])
            print(clusters[key]["CorrectReference"])
            print(clusters[key]["RevisedSentence"])

            for elem in clusters[key]["SelectedCentroids"]: 
                revised_untill_insertion = clusters[key]["revised_untill_insertion"]

                if "revised_after_insertion" in clusters[key].keys(): 
                    revised_after_insertion = clusters[key]["revised_after_insertion"]
                else: 
                    revised_after_insertion = clusters[key]["revised_afer_insertion"]


                context_before = remove_hashes(data_with_context[key]["ContextBefore"])
                line_to_write = "{0} <u>{1}</u> {2}".format(revised_untill_insertion, elem, revised_after_insertion)
                print(data_with_context[key]["ContextAfter"])
    print(counter)
        
main()