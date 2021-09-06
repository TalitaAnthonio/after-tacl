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


PATH_TO_FILTERED = "../coreference/filtered_train_preds_final_nouns_only_new_v2.json"
PATH_TO_MAIN = "../get-context/filtered_set_train_articles_tokenized_context_latest_with_context.json"
PATH_TO_CLUSTERS = "../word-embeddings/k_means_train_set_filtered_latest_new.json" 
BATCH_NR = 1
filename_to_write = "implicit_references_batch{0}_all_columns.csv".format(BATCH_NR)

with open(PATH_TO_MAIN, "r") as json_in: 
     data = json.load(json_in)

with open(PATH_TO_CLUSTERS, "r") as json_in: 
     clusters = json.load(json_in)


with open(PATH_TO_FILTERED, "r") as json_in: 
     filtered = json.load(json_in)
 

def format_title(title): 
    return "How to {0}".format(title.replace("_", " ").strip(".txt"))

def format_paragaph(par): 
    par_with_breaklines = []
    for index, sent in enumerate(par, 0):
        if index == 0: 
           formatted_sent = "<b>" + " " + sent + " " + "</b>" + "<br>"
        else: 
           formatted_sent = sent + " " + "<br>"
        par_with_breaklines.append(formatted_sent)

    return par_with_breaklines


# TODO: remove the ## in the title. 
def remove_hashes(paragraph_before): 
    cleaned = []
    for index, sent in enumerate(paragraph_before,0): 
        if index == 0: 
           sent = sent.replace("#", "")
        cleaned.append(sent)
    return cleaned 

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
    

    print(revised_before_insertion)
    print("==================================")
    
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

    d  = {"Title": [], "ContextBefore": [], "ContextAfter": [], "Sent": [], "PatternName": [], "Clusters": [], "Id": [], "FilteredPredictions": [], "Reference": []} 
    #d = {"Title": [], "ContextBefore": [], "ContextAfter": [], "Sent": [], "PatternName": [], "Id": []}

    for key, _ in data.items(): 
        if len(clusters[key]["SelectedCentroids"]) == 5: 
            revision_object = RevisionInstance(data, key, clusters)
            context_before = revision_object.context_before
            context_after = revision_object.context_after 
            formatted_context_before = format_paragaph(context_before)
            formatted_title = format_title(revision_object.filename) 

          

        



            if type(data[key]["reference"]) == list: 
                reference = " ".join(data[key]["reference"])
            else: 
                reference = data[key]["reference"]
           


            #print(formatted_title)
            #for sent in formatted_context_before: 
            #    print(sent)
            #print(context_after)
            
            #print("---------- clusters ---------- ")
            selected_centroids = clusters[key]["SelectedCentroids"]

            # make sure that the reference is in the centroids. 
            to_exclude = False
            for elem in selected_centroids: 
                if elem.startswith("."): 
                   to_exclude = True 
                   break 
                else: 
                    to_exclude = False 

        
            if reference.lower() in selected_centroids and to_exclude == False and formatted_context_before != [] and " ".join(context_before).startswith("#"): 
                revised_before_insertion = format_revised_before_insertion(revision_object.original_sentence, revision_object.original_in_article, revision_object.revised_before_insertion)
                
                fillers = selected_centroids
                random.shuffle(fillers)
                formatted_fillers = ["{0}{1}{2}".format("<u>", filler, "</u>") for filler in fillers]
                #print(formatted_fillers)

                # To select batches --> to do later  
                # minus 
                batch_nr = BATCH_NR-1
                sent = revised_before_insertion + " " + formatted_fillers[batch_nr] + " " + revision_object.revised_after_insertion + "<br>"
                sent = sent.replace(" .", ".").replace(" ,", ",").replace(" '", "'").replace(" ?", "?").replace(" !", "!").replace(" :", ":").replace(" ;", ";").replace(' "', '"') 
                
                
                
                sent = sent.replace("ca n’t", "can’t").replace("do n’t", "don’t").replace("does n’t", "doesn’t").replace("is n’t", "isn’t").replace("are n’t", "aren’t").replace(" ’re", "’re")
                sent = sent.replace("Ca n’t", "can’t").replace("Do n’t", "don’t").replace("Does n’t", "doesn’t").replace("Is n’t", "Isn’t").replace("Are n’t", "Aren’t")



                print("current", sent)
                
                d["Sent"].append(sent)
                  
                d["Id"].append(key)

                d["ContextBefore"].append(" ".join(remove_hashes( formatted_context_before)))
                
                d["PatternName"].append("implicit_references")
                d["Title"].append(formatted_title)
                d["FilteredPredictions"].append(filtered[key]["filtered_fillers2"])
                d["Reference"].append(reference)
                d["Clusters"].append(formatted_fillers)
                

                if context_after.startswith("#"): 
                    context_after = "<br>"

                
                d["ContextAfter"].append(context_after)

                if reference.lower() not in selected_centroids: 
                    print(data[key]["reference"])
                    print(key)
                    print(selected_centroids, reference) 
                    print("=================")
                    


    df = pd.DataFrame.from_dict(d)
    print(df)


    df.head(1000).to_csv(filename_to_write, index=False)


main()