import pandas as pd 
import re 
import json 
import random
import pdb 


PATH_TO_FILTERED = "../coreference/filtered_train_preds_final_nouns_only_new_v2.json"
PATH_TO_MAIN = "../get-context/filtered_set_train_articles_tokenized_context_latest_with_context.json"
PATH_TO_CLUSTERS = "../word-embeddings/k_means_train_set_filtered_latest_new.json" 
BATCH_NR = 5
filename_to_write = "implicit_references_batch{0}.csv".format(BATCH_NR)

with open(PATH_TO_MAIN, "r") as json_in: 
     data = json.load(json_in)

with open(PATH_TO_CLUSTERS, "r") as json_in: 
     clusters = json.load(json_in)


with open(PATH_TO_FILTERED, "r") as json_in: 
     filtered = json.load(json_in)

import pickle 
with open("dict_with_fillers.pickle", "rb") as pickle_in: 
     dict_with_fillers = pickle.load(pickle_in)


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
    

    
    return revised_before_insertion
    

def replacement(string): 
    string = string.replace(" .", ".").replace(" ,", ",").replace(" '", "'").replace(" ?", "?").replace(" !", "!").replace(" :", ":").replace(" ;", ";").replace(' "', '"') 
    string = string.replace("ca n’t", "can’t").replace("do n’t", "don’t").replace("does n’t", "doesn’t").replace("is n’t", "isn’t").replace("are n’t", "aren’t").replace(" ’re", "’re")
    string = string.replace("Ca n’t", "can’t").replace("Do n’t", "don’t").replace("Does n’t", "doesn’t").replace("Is n’t", "Isn’t").replace("Are n’t", "Aren’t")
    return string 

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

    #d  = {"Title": [], "ContextBefore": [], "ContextAfter": [], "Sent": [], "PatternName": [], "Clusters": [], "Id": [], "FilteredPredictions": [], "Reference": []} 
    d = {"Title": [], "ContextBefore": [], "ContextAfter": [], "Sent": [], "PatternName": [], "Id": [], "BatchNr": []}

    counter = 0 
    # make sure to only use those that we have tried before 
    for key, _ in dict_with_fillers.items(): 
       
            revision_object = RevisionInstance(data, key, clusters)
            context_before = revision_object.context_before
            context_after = revision_object.context_after 
            formatted_context_before = format_paragaph(context_before)
            formatted_title = format_title(revision_object.filename) 
            revised_before_insertion = format_revised_before_insertion(revision_object.original_sentence, revision_object.original_in_article, revision_object.revised_before_insertion)
            
            fillers =  clusters[key]["SelectedCentroids"]
            #pdb.set_trace()
            if len(fillers) != len(set(clusters[key]["SelectedCentroids"])): 
               counter +=1 
               print(key, fillers)
    
    print(counter)
            
main()