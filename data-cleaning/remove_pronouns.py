# Merge the files with embeddings and clusters together 

import json 
import pdb 


PATH_TO_FILE = "../coreference/filtered_train_preds_final_nouns_only.json"

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)


with open("../../tacl/data/references_for_lm.json", "r") as json_in: 
     all_data = json.load(json_in)




def check_filler_length(fillers, reference): 
    fillers_without_reference = [filler for filler in fillers if filler.lower() != reference.lower()]
    if len(fillers_without_reference) <= 4: 
        return 0
    else: 
        return 1



unique_references = []
pronouns = ["all", '"', "i", "our", "we", "of", "yours", "it", "your", "he", "she", "him", "her", "they", "them", "these", ",", "their", "yourself", "me", "its", "herself", "you"]
counter = 0 
filtered_set = {}
filenames = []
for key, _ in data.items(): 
    reference = data[key]['reference']
    filtered_fillers = data[key]["filtered_fillers"]

    if type(reference) != str:
        reference = ' '.join(data[key]['reference']) 
    


    to_keep = check_filler_length(filtered_fillers, reference)
    if to_keep == 1: 



        if data[key]['reference-type'] == 'unigram':
            if reference.lower() not in pronouns: 
                unique_references.append(reference)
                filtered_set[key] = data[key]
                filtered_set[key].update({"Filename": all_data[key]["filename"]})
                filenames.append(all_data[key]["filename"])
 
        else: 
            unique_references.append(reference)
            filtered_set[key] = data[key]
            filtered_set[key].update({"Filename": all_data[key]["filename"]})
            print(all_data[key]["filename"])
 
        

filenames = list(set(filenames))
for elem in filenames: 
    print(elem)
    


    # check the length of the fillers 

