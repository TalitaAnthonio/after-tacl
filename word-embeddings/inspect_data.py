import json 
import pickle 
import pdb 


PATH_TO_EMBEDDINGS = "bert_vectors_FINAL_dev_top100_nouns_only.pickle"
PATH_TO_FILE_CLUSTERS = "kmeans_k=5_dev.json"


PATH_TO_FILE = "../coreference/filtered_dev_preds_final_nouns_only.json"

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)


with open(PATH_TO_EMBEDDINGS, "rb") as pickle_in: 
     embeddings = pickle.load(pickle_in) 

with open(PATH_TO_FILE_CLUSTERS, "r") as json_in: 
     clusters = json.load(json_in)


for key, _ in clusters.items(): 
    if key == "Succeed_with_Women32": 
          print(data[key]['RevisedSentence'])
          filtered = embeddings[key]["filtered_fillers"]

          all_predictions = data[key]['GPT+Finetuning+P-perplexityPred']

          print(all_predictions)
          print(filtered)


