# script to analyse the fillers. 
import json 
import pdb 
import spacy 
from tools import count_tags
from collections import Counter 
import numpy as np 

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


def make_freqdict(list_of_countable_elements): 
    freq_dict = Counter() 
    for elem in list_of_countable_elements: 
        freq_dict[elem] +=1 
    return dict(freq_dict) 

def main(): 

    all_tags = Counter() 

    total = []
    for key, _ in file_with_predictions.items(): 
        revision_object = Revisioninstance(key, file_with_predictions[key])

        best_model_predictions = revision_object.best_model_predictions
        all_fillers = revision_object.all_fillers
        pos_tags, tokens = count_tags(revision_object.pos_tagged_fillers)
        freq_dict = make_freqdict(pos_tags)
        
        print(freq_dict)
        for pos, freq in freq_dict.items():
            if len(pos.split()) == 1:  
                all_tags[pos] += freq_dict[pos]
                total.append(freq_dict[pos])

        print(revision_object.pos_tagged_fillers)
        

    
    total_fillers = np.sum(total)

    all_tags_avg = {k:(v/total_fillers) for k, v in all_tags.items()}
    all_tags_avg = {k: v for k, v in sorted(all_tags_avg.items(), key=lambda item: item[1], reverse=True)}
    print("========= average =======")
    print(all_tags_avg)
main()

