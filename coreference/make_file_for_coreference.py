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

    def __init__(self, wikihow_id): 
        self.wikihow_id = wikihow_id
    

    @property 
    def predictions(self): 
        predictions = [prediction.strip() for prediction in file_with_predictions[self.wikihow_id]["GPT+Finetuning+P-perplexityPred"]]
        return predictions 


def main(): 
    development_set = {key: value for key, value in references_for_lm.items() if references_for_lm[key]["Split"] == "DEV"}
    

    for key, _ in development_set.items(): 
        predictions = WikihowRev(key).predictions
        print("predictions", predictions)
           

main()