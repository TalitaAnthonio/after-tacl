# Make a test set file with the predictions and the rest together. 

import json 
import pdb 


TestPredictions = "/Users/talita/Documents/PhD/tacl/language-modeling/results-on-test-set-reranked-context-finetuned.json"

with open("../../tacl/data/references_for_lm.json", "r") as json_in: 
     all_data = json.load(json_in)

with open(TestPredictions, "r") as json_in: 
     predictions = json.load(json_in)

counter = 0 
d = {}
for key, _ in all_data.items(): 
    if all_data[key]['Split'] == 'TEST': 
       counter +=1 
       # get the predictions from the lm 
       preds_by_lm = [pred.strip() for pred in predictions[key]["predictions"]["generated_texts"]]
       if 'coref' in all_data[key].keys(): 
            del all_data[key]['coref']
            del all_data[key]['sents']
        
       d[key] = all_data[key]
       d[key].update({"predictions": preds_by_lm})
print(counter)

with open("test_set_all_info.json", "w") as json_out: 
     json.dump(d, json_out)

