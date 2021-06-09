# Script to remove the entities that are the same. 

import json 
import numpy as np 
import pdb 
import pandas as pd 

path_to_pred_dir = "/Users/talita/Documents/PhD/tacl/analyse-predictions" 
path_to_file_with_predictions = '{0}/bestmodels_predictions.json'.format(path_to_pred_dir)
path_to_filtered_fillers = "../coreference/dev_set_with_filtered_fillers.json"

with open(path_to_file_with_predictions, "r") as json_in: 
     data = json.load(json_in)


with open(path_to_filtered_fillers, "r") as json_in: 
     filtered_fillers = json.load(json_in)

with open("../word-embeddings/dev_set_references.json", "r") as json_in: 
     references = json.load(json_in)


class RevisionInstance: 

    # revision_instance = data[key]
    def __init__(self, key, revision_instance, keys):
        self.revision_instance = revision_instance
        self.key = key 
        self.keys = keys 
        self.left_context = revision_instance["LeftContext"]
        self.predictions = [prediction.strip() for prediction in revision_instance["GPT+Finetuning+P-perplexityPred"]]
        self.filtered_fillers = filtered_fillers[key]["filtered_fillers"]
        self.revised_after_insertion = revision_instance["revised_after_insertion"]
        self.reference_type = revision_instance["reference-type"]

    @property 
    def revised_untill_insertion(self): 
        if "revised_untill_insertion" in self.keys: 
           return self.revision_instance["revised_untill_insertion"]
        else: 
           return self.revision_instance["revised_until_insertion"]

    #@property 
    #def dict_with_fillers(self): 


def filter_second_step(filtered_fillers): 
    d = {}

    for elem in filtered_fillers: 
        if len(elem.split()) == 2: 
            noun = elem.split()[1]
        elif len(elem.split()) == 3: 
            noun = elem.split()[2]
        else: 
            noun = elem 
        if noun in d.keys(): 
            d[noun].append(elem) 
        else: 
            d[noun] = []
            d[noun].append(elem)

    return d 


def main(): 

    d = {"id": [], "revised_sentence": [], "human-inserted": [], "predictions": [], "filtered1": [], "filtered2": [], "coref-entities": [], "context": [], "revision-type":[]}

    dict_for_json = {}
    for key, _ in data.items(): 
        revision_object = RevisionInstance(key, data[key], data[key].keys())
        print("================================")
        print(data[key]["RevisedSentence"])

        #if revision_object.reference_type == "trigram" or revision_object.reference_type == "bigram": 
        filtered = filter_second_step(revision_object.filtered_fillers)

        fillers_to_keep = []
        for noun, _ in filtered.items(): 
            if noun not in ["the", "a", "to"]: 
                if data[key]["CorrectReference"].lower() in filtered[noun]: 
                    fillers_to_keep.append(data[key]["CorrectReference"].lower())
                else: 
                    fillers_to_keep.append(filtered[noun][0])


        context = revision_object.left_context
        predictions = revision_object.predictions
        reference_type = revision_object.reference_type
        revised_sentence = data[key]["RevisedSentence"]
        filtered_fillers = revision_object.filtered_fillers
        new_filtered = fillers_to_keep 

        
        # make df  
        d["id"].append(key)
        d["revised_sentence"].append(revised_sentence)
        d["human-inserted"].append(data[key]["CorrectReference"])
        d["predictions"].append(predictions)
        d["filtered1"].append(filtered_fillers)
        d["filtered2"].append(fillers_to_keep)
        d["context"].append(context)
        d["revision-type"].append(revision_object.reference_type)
        d["coref-entities"].append(references[key]["unique_references_in_context"])


        df = pd.DataFrame.from_dict(d)
        df.to_csv("current_filtered_set.tsv", sep='\t', index=False)

        # make for json 
        dict_for_json[key] = {"revised_sentence": revised_sentence, "predictions": predictions, "CorrectReference": data[key]["CorrectReference"], 
         "filtered1": filtered_fillers, "filtered2": fillers_to_keep, "context": context, "revision-type": revision_object.reference_type, 
         "revised_untill_insertion": revision_object.revised_untill_insertion, "revised_after_insertion": data[key]["revised_after_insertion"], 
         "coref-entities": references[key]["unique_references_in_context"], "par": data[key]["par"]}


        with open("filtered_predictions_step2.json", "w") as json_out: 
             json.dump(dict_for_json, json_out)

main()