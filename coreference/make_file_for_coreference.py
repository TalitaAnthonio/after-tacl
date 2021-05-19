# This script is used to make a file with the following format. 
# id: {"fillers": {"filler_name1": [""], {"filler_name2": ["the sentence"]} }}


import json 
import pdb 

# paths to files 
path_to_pred_dir = "/Users/talita/Documents/PhD/tacl/analyse-predictions"

path_to_file_with_predictions = '{0}/bestmodels_predictions.json'.format(path_to_pred_dir)

with open(path_to_file_with_predictions, "r") as json_in: 
     file_with_predictions = json.load(json_in)

with open('/Users/talita/Documents/PhD/tacl/data/references_for_lm.json', 'r') as json_in: 
     references_for_lm = json.load(json_in)
     

class WikihowRev: 

    def __init__(self, wikihow_id, wikihow_instance): 
        self.wikihow_id = wikihow_id
        self.wikihow_instance = wikihow_instance
    

    @property 
    def predictions(self): 
        predictions = [prediction.strip() for prediction in file_with_predictions[self.wikihow_id]["GPT+Finetuning+P-perplexityPred"]]
        return predictions 
    
    @property 
    def revised_after_insertion(self): 
        if "revised_after_insertion" in self.wikihow_instance.keys(): 
            revised_after_insertion = self.wikihow_instance["revised_after_insertion"]
        else: 
            revised_after_insertion = self.wikihow_instance["revised_afer_insertion"]

        return revised_after_insertion
    
    @property 
    def reference(self): 
        reference = self.wikihow_instance["reference"]
        if type(reference) == list: 
           return " ".join(reference)
        else: 
           return reference 


def main(): 
    development_set = {key: value for key, value in references_for_lm.items() if references_for_lm[key]["Split"] == "DEV"}
    

    collection = {}
    for key, _ in development_set.items(): 
        wikihow_instance = WikihowRev(key, development_set[key])
        predictions = wikihow_instance.predictions
        revised_after_insertion = wikihow_instance.revised_after_insertion
        revised_before_insertion = development_set[key]["revised_untill_insertion"]
        reference = wikihow_instance.reference
    

        # TODO: if the reference is not in predictions, then add to it. 
        dict_with_fillers = {"fillers": {}}
        for rank, prediction in enumerate(predictions,1): 
            sentence_with_filler = revised_before_insertion + " " + prediction + " " + revised_after_insertion
            dict_with_fillers["fillers"][prediction] = {"sentence": sentence_with_filler, "rank": rank}
            
        
        collection[key] = dict_with_fillers
        collection[key].update({"par": development_set[key]["par"], "reference": reference})

        
    
    with open("coreference_analysis_predictions_dev_set.json", "w") as json_out: 
         json.dump(collection, json_out)
        

           

main()