# make csv with clusters 
# distribution: Counter({5: 576, 1: 14, 2: 1})

import json
from os import read
from numpy import trunc 
import pandas as pd 
import pdb 
from collections import Counter

PATH_TO_FILE = "../coreference/filtered_dev_preds_final.json"
NUM_OF_PRED = 20
PATH_TO_CLUSTERS = "../word-embeddings/kmeans_k=5_filtered_step1_top{0}_with_rev_v2.json".format(NUM_OF_PRED)
PATH_TO_FILE_OUT = "./amazon_file.csv"

with open(PATH_TO_CLUSTERS, "r") as json_in: 
     clusters = json.load(json_in)
 

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)


with open("../../tacl/data/references_for_lm.json", "r") as json_in: 
     all_data = json.load(json_in)

def format_text(title): 
    return "<b> How to {0} </b>".format(title.replace("_", " ").strip(".txt"))

def trunc_par(par):
    #print(data[key]["par"])
    par = par.strip('\n').split('\n')[-6:]

    formatted = []
    for sent in par: 
        par_with_newline = sent + '\n'
        formatted.append(par_with_newline)

    return formatted 

def main(): 

    d  = {"Title": [], "Context": [], "Sent": [], "Reference": []} 
    for key, _ in data.items(): 
        if len(clusters[key]["Centroids_with_revised"]) == 5: 
            d["Title"].append(format_text(all_data[key]["filename"]))
            formatted = " ".join(trunc_par(data[key]["par"]))
            d["Context"].append(formatted.replace('\n', "<br>"))
            d["Sent"].append(data[key]["RevisedSentence"])
            d["Reference"].append(all_data[key]["reference"])
            


    df = pd.DataFrame.from_dict(d)
    df = df.tail(10)
    df.tail(10).to_csv(PATH_TO_FILE_OUT, index=False)

main()