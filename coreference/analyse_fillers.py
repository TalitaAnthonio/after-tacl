# script to analyse the fillers. 
import json 
import pdb 
import spacy 

MODEL = spacy.load('en_core_web_sm')


path_to_pred_dir = "/Users/talita/Documents/PhD/tacl/analyse-predictions" 
path_to_file_with_predictions = '{0}/bestmodels_predictions.json'.format(path_to_pred_dir)

with open(path_to_file_with_predictions, "r") as json_in: 
     file_with_predictions = json.load(json_in)


class Revisioninstance: 
    def __init__(self, instance_id, revision_instance):
        self.revision_instance = revision_instance
        self.instance_id = instance_id

    @property 
    def best_model_predictions(self): 
        return [filler.strip() for filler in self.revision_instance["GPT+Finetuning+P-perplexityPred"]]
    

    @property 
    def correct_ref(self): 
        return self.revision_instance['CorrectReference']
    

    # fillers including the revision 
    @property
    def all_fillers(self):     
        correct_ref = self.revision_instance['CorrectReference']
        predictions = [filler.strip().lower() for filler in self.revision_instance["GPT+Finetuning+P-perplexityPred"]]
        if correct_ref in predictions: 
           return [filler.strip().lower() for filler in self.revision_instance["GPT+Finetuning+P-perplexityPred"]]
        else: 
          predictions = [filler.strip().lower() for filler in self.revision_instance["GPT+Finetuning+P-perplexityPred"]]
          predictions.append(correct_ref)
          return predictions


    @property 
    def pos_tagged_fillers(self): 
        predictions = [filler.strip() for filler in self.revision_instance["GPT+Finetuning+P-perplexityPred"]]
        
        tagged_fillers = []
        for filler in predictions: 
            tagged = MODEL(filler)
            pos_tagged = [[token.text, token.tag_] for token in tagged]
            tagged_fillers.append(pos_tagged)
        return tagged_fillers
    
    @property
    def pos_tagged_fillers_all(self): 
        predictions = self.all_fillers
        
        tagged_fillers = []
        for filler in predictions: 
            tagged = MODEL(filler)
            pos_tagged = [[token.text, token.tag_] for token in tagged]
            tagged_fillers.append(pos_tagged)
        return tagged_fillers


def main(): 
    for key, _ in file_with_predictions.items(): 
        revision_object = Revisioninstance(key, file_with_predictions[key])

        best_model_predictions = revision_object.best_model_predictions
        all_fillers = revision_object.all_fillers
        if revision_object.pos_tagged_fillers != revision_object.pos_tagged_fillers_all: 
           print(revision_object.pos_tagged_fillers, '\n', revision_object.pos_tagged_fillers_all) 
           print("=======================================================")


main()

