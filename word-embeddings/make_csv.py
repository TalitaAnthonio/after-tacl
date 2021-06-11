# make csv with clusters 
# distribution: Counter({5: 576, 1: 14, 2: 1})

import json
from os import read 
import pandas as pd 
import pdb 
from collections import Counter

PATH_TO_CLUSTERS = "kmeans_k=5_filtered_step1_top20.json"
PATH_TO_FILE = "../coreference/filtered_predictions_step2.json"

with open(PATH_TO_CLUSTERS, "r") as json_in: 
     clusters = json.load(json_in)
 

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)


def main(): 

    d = {"Id": [], "RevisedSentence": [], "Paragraph": [], "Reference": [],  "Cluster0": [], "Cluster1": [], "Cluster2": [], "Cluster3": [], "Cluster4": [], "Centroids": []}
    
    freqdict = Counter()
    lens = []
    for key, _ in data.items(): 
        d["RevisedSentence"].append(data[key]["revised_sentence"])
        d["Reference"].append(data[key]["CorrectReference"])
        d["Paragraph"].append(data[key]["par"])
        d["Id"].append(key)

    
        sents_for_0 = []
        sents_for_1 = []
        sents_for_2 = []
        sents_for_3 = []
        sents_for_4 = []
        for k, _ in clusters[key]["clusters"].items(): 
            for sent in clusters[key]["clusters"][k]: 
                sent = sent + "\n"
                if k == "0": 
                    sents_for_0.append(sent)

                elif k=="1": 
                    sents_for_1.append(sent)
                
                elif k=="2": 
                    sents_for_2.append(sent)
                
                elif k == "3": 
                    sents_for_3.append(sent)
                
                elif k == "4": 
                    sents_for_4.append(sent)
        

        
        d["Cluster0"].append(" ".join(sents_for_0).strip('\n'))
        d["Cluster1"].append(" ".join(sents_for_1))
        d["Cluster2"].append(" ".join(sents_for_2))
        d["Cluster3"].append(" ".join(sents_for_3))
        d["Cluster4"].append(" ".join(sents_for_4))

        #pdb.set_trace()


        centroids = " ".join([cluster + "\n" for cluster in clusters[key]["centroids"]])
        d["Centroids"].append(centroids)

        lens.append(len(clusters[key]["centroids"]))

    
    for l in lens: 
         freqdict[l] +=1 
    

    print(freqdict)


    df = pd.DataFrame.from_dict(d)
    df.to_csv("clusters_5_top20.tsv", sep='\t', index=False)

main()