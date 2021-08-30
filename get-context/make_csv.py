import json 
import pandas as pd 
import pdb 

with open("train_set_with_context_subset.json", "r") as json_in: 
     data = json.load(json_in)

with open("../word-embeddings/kmeans_k=5_dev.json", "r") as json_in: 
     clusters = json.load(json_in)

d = {"Filename": [], "BaseSentence": [],  "RevisedSentence": [], "Reference": [],  "FullParagraph": [], "ContextForAnnotation": []}
for key, _ in data.items(): 

    print(data[key]["Split"])
    d["Filename"].append(data[key]["Filename"])
    d["FullParagraph"].append(data[key]["FullParagraph"]) 
    if "BaseSentence" in data[key].keys(): 
        d["BaseSentence"].append(data[key]["BaseSentence"])
    else: 
        if "Base_Sentence" in data[key].keys(): 
            d["BaseSentence"].append(data[key]["Base_Sentence"])
        else: 
            d["BaseSentence"].append(" ".join(data[key]["base_tokenized"]))
    d["RevisedSentence"].append(data[key]["revised_sentence"])
    d["ContextForAnnotation"].append(data[key]["ContextForAnnotation"])
    d["Reference"].append(data[key]["Reference"]) 
    #d["Fillers"].append(clusters[key]["Centroids_with_revised"])


df = pd.DataFrame.from_dict(d)
print(df)
df.to_csv("train_set_with_context.tsv", sep='\t', index=False)