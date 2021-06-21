import json 
import pdb 


PATH_TO_FILE = "../coreference/filtered_dev_preds_final.json"
NUM_OF_PRED = 20 
PATH_TO_CLUSTERS = "kmeans_k=5_filtered_step1_top{0}_with_rev_v2.json".format(NUM_OF_PRED)

with open(PATH_TO_CLUSTERS, "r") as json_in: 
     clusters = json.load(json_in)
 

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)


for key, _ in data.items(): 
    preds = clusters[key]["Centroids_with_revised"]
    print(preds)

    revised_sentence = data[key]["RevisedSentence"]
    if "revised_untill_insertion" in data[key].keys(): 
        revised_untill_insertion = data[key]["revised_untill_insertion"]
    else: 
        revised_untill_insertion = data[key]["revised_until_insertion"]
    revised_sentence_alt = revised_untill_insertion + " " + data[key]["CorrectReference"] + " " + data[key]["revised_after_insertion"]  
    
    if revised_sentence_alt or revised_sentence in preds: 
       print('correct')
    else: 
        pdb.set_trace()