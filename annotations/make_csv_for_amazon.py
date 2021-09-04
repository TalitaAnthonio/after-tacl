# make csv with clusters 
# distribution: Counter({5: 576, 1: 14, 2: 1})


import json
from os import read
from nltk.util import Index
from numpy import average, trunc 
import pandas as pd 
import pdb 
from collections import Counter
import numpy as np 
import pdb 
import re 
import random 


PATH_TO_MAIN = "../get-context/filtered_set_train_articles_tokenized_context_latest_with_context.json"
PATH_TO_CLUSTERS = "../word-embeddings/k_means_train_set_filtered_latest_new.json" 


with open(PATH_TO_MAIN, "r") as json_in: 
     data = json.load(json_in)

with open(PATH_TO_CLUSTERS, "r") as json_in: 
     clusters = json.load(json_in)


def format_title(title): 
    return "How to {0}".format(title.replace("_", " ").strip(".txt"))

def format_paragaph(par): 
    par_with_breaklines = []
    for index, sent in enumerate(par, 0):
        if index == 0: 
           formatted_sent = "<b>" + " " + sent + " " + "</b>" 
        else: 
           formatted_sent = sent + " " + "<br>"
        par_with_breaklines.append(formatted_sent)

    return par_with_breaklines


def format_revised_before_insertion(original_sentence, original_sentence_in_raw, revised_before_insertion): 
    """ 

        Original sentence: the sentence as given in the tsv file 
        original_sentence_in_raw : the sentence in the article 
        revised_before_insertion {str}: the part before the insertion
    """

    starts_with_bullet_point = re.findall(r"^[0-9]+\.", original_sentence_in_raw[0])
   
    if starts_with_bullet_point: 
       original_sentence = " ".join(starts_with_bullet_point) + " " + original_sentence
       revised_before_insertion = " ".join(starts_with_bullet_point) + " " + revised_before_insertion
    elif original_sentence_in_raw[0].startswith("* "): 
        original_sentence = "* " + original_sentence
        revised_before_insertion = "* " + revised_before_insertion
    
    else: 
        original_sentence = original_sentence
        revised_before_insertion = revised_before_insertion
    return revised_before_insertion
    

    


class RevisionInstance: 

    def __init__(self, instance, key, clusters): 

        self.instance = instance 
        self.key = key 
        self.clusters = clusters 
        self.filename = instance[key]["filename"]

        self.centroids_with_revised = clusters

        self.context_before = instance[key]["ContextBefore"]
        self.context_after = " ".join(instance[key]["ContextAfter"]) 


        self.revised_before_insertion = instance[key]["RevisedBeforeInsertion"]
        self.revised_after_insertion = instance[key]["RevisedAfterInsertion"]
        self.original_in_article = data[key]["Tokenized_article"]["current"]
        self.reference = data[key]["Reference"]

        
        if "BaseSentence" not in instance[key].keys(): 
               
               try: 
                    self.original_sentence = data[key]["Base_Sentence"]
               except KeyError: 
                   self.original_sentence = " ".join(data[key]["base_tokenized"])
                   
              
        else: 
            self.original_sentence = data[key]["BaseSentence"]




def main(): 

    d  = {"Title": [], "ContextBefore": [], "ContextAfter": [], "Sent": [], "PatternName": [], "Clusters": [], "Id": [], "FilteredPredictions": []} 

    for key, _ in data.items(): 
        pdb.set_trace()
        revision_object = RevisionInstance(data, key, clusters)
        context_before = revision_object.context_before
        context_after = revision_object.context_after 
        formatted_context_before = format_paragaph(context_before)
        formatted_title = format_title(revision_object.filename) 

        
        d["Id"].append(key)
        d["ContextBefore"].append(" ".join(context_before))
        d["ContextAfter"].append(context_after)
        d["PatternName"].append("implicit_references")
        d["Title"].append(formatted_title)
        d["FilteredPredictions"].append(data[key]["FilteredPredictions"])


        print(formatted_title)
        for sent in formatted_context_before: 
            print(sent)
        print(context_after)
        
        print("---------- clusters ---------- ")
        selected_centroids = clusters[key]["SelectedCentroids"]

        revised_before_insertion = format_revised_before_insertion(revision_object.original_sentence, revision_object.original_in_article, revision_object.revised_before_insertion)
        
        fillers = selected_centroids + [revision_object.reference]
        random.shuffle(fillers)
        formatted_fillers = ["{0}{1}{2}".format("<u>", filler, "</u>") for filler in fillers]
        print(formatted_fillers)

        # To select batches --> to do later  
        batch_nr = 1 
        sent = revised_before_insertion + formatted_fillers[batch_nr] + revision_object.revised_after_insertion
        
        d["Sent"].append(sent)
        d["Clusters"].append(formatted_fillers)


    df = pd.DataFrame.from_dict(d)
    print(df)
    df.to_csv("implicit_references.tsv", sep='\t')


main()