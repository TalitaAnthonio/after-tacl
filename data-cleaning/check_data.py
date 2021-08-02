import json 
import pdb 
from collections import Counter 
import spacy 

spacy_model = spacy.load("en_core_web_sm")

with open("all_references.json", "r") as json_in: 
     data = json.load(json_in)


def get_pos_tags(filler): 
    parsed = spacy_model(filler)
    return [token.tag_ for token in parsed]


for key, _ in data.items(): 
    tagged_reference = get_pos_tags(data[key]["Reference"]) 
    
    if tagged_reference != ['PRP'] and tagged_reference != ['PRP$']: 
        print(data[key]["Filename"])
        print(data[key]["Par"])
        print("------------")
        print(data[key]["RevisedSentence"])
        print(data[key]["Reference"])
        print(data[key]["predictions"])
        print("====================================")
    
    
    