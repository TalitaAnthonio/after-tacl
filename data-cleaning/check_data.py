import json 
import pdb 
from collections import Counter 
import spacy 

 # 1428, 'you': 1040,
spacy_model = spacy.load("en_core_web_sm")


def get_pos_tags(filler): 
    parsed = spacy_model(filler)
    return [token.tag_ for token in parsed]

with open("../../tacl/data/references_for_lm.json", "r") as json_in: 
     all_data = json.load(json_in)

# count how many references there are 
freq_dict = Counter()
references = [" ".join(all_data[key]['reference']).lower() if type(all_data[key]["reference"]) == list else all_data[key]['reference'] for key, _ in all_data.items()]

# exclude references 
for key, _ in all_data.items(): 
    if type(all_data[key]["reference"]) == list: 
        reference = " ".join(all_data[key]['reference']) 
    else: 
        reference = all_data[key]["reference"]
    tagged_reference = get_pos_tags(reference)

    if tagged_reference != ['PRP'] and tagged_reference != ['PRP$']: 
        print(tagged_reference, reference)
