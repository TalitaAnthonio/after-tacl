import json 
import pdb 
from collections import Counter 
import spacy 

 # 1428, 'you': 1040,
spacy_model = spacy.load("en_core_web_sm")


# file with predictions 
PATH_TO_DEV_FILE_PRED = "../coreference/filtered_dev_preds_final.json"
PATH_TO_TRAIN_FILE_PRED = "../coreference/filtered_train_preds_final.json"


PATH_TO_OTHER_INFO = "./data/all_references.json"

with open(PATH_TO_OTHER_INFO, "r") as json_in: 
     file_with_all_info = json.load(json_in)


def get_pos_tags(filler): 
    parsed = spacy_model(filler)
    return [token.tag_ for token in parsed]

#with open("../../tacl/data/references_for_lm.json", "r") as json_in: 
#     all_data = json.load(json_in)


with open(PATH_TO_DEV_FILE_PRED, "r") as json_in: 
     predictions_data = json.load(json_in)

with open(PATH_TO_TRAIN_FILE_PRED, "r") as json_in: 
     predictions_train = json.load(json_in)

predictions_data.update(predictions_train)


# count how many references there are 
freq_dict = Counter()
try: 
    references = [" ".join(file_with_all_info[key]['Reference']).lower() if type(file_with_all_info[key]["Reference"]) == list else file_with_all_info[key]['Reference'] for key, _ in file_with_all_info.items()]

except KeyError: 
    pdb.set_trace()

# exclude references 
for key, _ in predictions_data.items(): 
    if type(file_with_all_info[key]["Reference"]) == list: 
        reference = " ".join(file_with_all_info[key]['reference']) 
    else: 
        reference = file_with_all_info[key]["Reference"]
    tagged_reference = get_pos_tags(reference)

    if tagged_reference != ['PRP'] and tagged_reference != ['PRP$']: 
        print(key)
        print(tagged_reference, reference)
 
        filtered_fillers = predictions_data[key]["filtered_fillers"]
  
        print(file_with_all_info[key]["Par"])
        print(file_with_all_info[key]["RevisedSentence"])
        print('\n')
        print("filtered fillers", filtered_fillers)
        print("reference", file_with_all_info[key]["Reference"])
        print("base_nr:", file_with_all_info[key]["BaseNr"])
        print("=========================================")

