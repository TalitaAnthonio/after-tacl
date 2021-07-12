import json 
import pdb 


PATH_TO_FILE = "../coreference/filtered_train_preds_final.json"
NUM_OF_PRED = 20 
PATH_TO_CLUSTERS = "kmeans_k=5_train.json".format(NUM_OF_PRED)

with open(PATH_TO_CLUSTERS, "r") as json_in: 
     clusters = json.load(json_in)
 

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)


for key, _ in data.items(): 
    preds = clusters[key]["Centroids_with_revised"]
    print(preds)

    revised_sentence = data[key]["revised_sentence"]
    if "revised_untill_insertion" in data[key].keys(): 
        revised_untill_insertion = data[key]["revised_untill_insertion"]
    else: 
        revised_untill_insertion = data[key]["revised_until_insertion"]
    
    reference = " ".join(data[key]["reference"])

    if 'revised_after_insertion' in data[key].keys(): 
        revised_after_insertion = data[key]["revised_after_insertion"]
    else: 
        revised_after_insertion = data[key]["revised_afer_insertion"]
    revised_sentence_alt = revised_untill_insertion + " " + reference + " " + revised_after_insertion
    
    if revised_sentence_alt or revised_sentence in preds: 
       print('correct')
    else: 
        pdb.set_trace()