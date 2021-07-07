import spacy 
import string 
import pdb 
import json 
import pickle 

MODEL = spacy.load('en_core_web_sm')
PUNCTUATION = string.punctuation + "..." + '(' + ')'

path_to_pred_dir = "/Users/talita/Documents/PhD/tacl/analyse-predictions" 
path_to_file_with_predictions = '{0}/bestmodels_predictions.json'.format(path_to_pred_dir)
path_to_filtered_fillers = "../coreference/dev_set_with_filtered_fillers.json"

with open(path_to_file_with_predictions, "r") as json_in: 
     data = json.load(json_in)

with open(path_to_filtered_fillers, "r") as json_in: 
     filtered = json.load(json_in)

with open("../word-embeddings/bert_vectors_POSTAG_newest.pickle", "rb") as pickle_in: 
     vectors = pickle.load(pickle_in)

s = "abc1"
contains_digit = any(map(str.isdigit, s))


for key, _ in data.items(): 
    if key == "Filter_Search_Results_on_Facebook12": 
       print(data[key]["GPT+Finetuning+P-perplexityPred"])
       print(filtered[key]["filtered_fillers"])
       print(data[key]["CorrectReference"])
       print(vectors[key]["sentences"])
       pdb.set_trace()

