# make csv with clusters 
# distribution: Counter({5: 576, 1: 14, 2: 1})

import json
from os import read 
import pandas as pd 
import pdb 
from collections import Counter

PATH_TO_FILE = "../coreference/filtered_dev_preds_final.json"
NUM_OF_PRED = 20
PATH_TO_CLUSTERS = "kmeans_k=5_filtered_step1_top{0}_with_rev_v2.json".format(NUM_OF_PRED)
PATH_TO_FILE_OUT = "amazon_file.csv"

with open(PATH_TO_CLUSTERS, "r") as json_in: 
     clusters = json.load(json_in)
 

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)



def main(): 

    d  = {"Title": [], "Context": [], "GapSent": [],  "Sent1": [], "Sent2": [], "Sent3": [], "Sent4": [], "Sent5": []}
    for key, _ in data.items(): 
        if len(clusters[key]["Centroids_with_revised"]) == 5: 
            d["Title"].append(key)
            d["Context"].append(data[key]["par"].replace('\n', "<br>"))
            if "revised_untill_insertion" in data[key].keys(): 
                revised_untill_insertion = data[key]["revised_untill_insertion"]
            else: 
                revised_untill_insertion = data[key]["revised_until_insertion"]

            line_with_gap = revised_untill_insertion + " " + "__________" + " " + data[key]["revised_after_insertion"]
 
            d["GapSent"].append(line_with_gap)
            for pos, elem in enumerate(clusters[key]["Centroids_with_revised"],1): 
                key_to_append = "Sent{0}".format(str(pos))
                d[key_to_append].append(elem)
        



    df = pd.DataFrame.from_dict(d)
    df = df.head(10)
    df.head(10).to_csv(PATH_TO_FILE_OUT, index=False)

main()