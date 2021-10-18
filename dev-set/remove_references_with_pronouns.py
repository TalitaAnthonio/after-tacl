import json 
import pickle 

PATH_TO_FILE = "../coreference/filtered_dev_preds_final_nouns_only.json"

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)
    

pronouns = ["all", '"', "=", "itself", "us", "2004", "i", "our", "we", "of", "yours", "it", "your", "he", "she", "him", "her", "they", "them", "these", ",", "their", "yourself", "me", "its", "herself", "you"]
list_with_non_pronouns = []
for key, _ in data.items(): 
    correct_reference = data[key]['CorrectReference']
    if correct_reference.lower() not in pronouns: 
       list_with_non_pronouns.append(key) 
       print(correct_reference)


print(len(list_with_non_pronouns))

with open("human_inserted_reference_not_pronoun.pickle", "wb") as pickle_out: 
     pickle.dump(list_with_non_pronouns, pickle_out)

