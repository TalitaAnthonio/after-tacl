# Script used to filter the generated fillers from GPT+Paragraph Perplexity in Step 1. 

import json 
import pdb 
import spacy 
from tools import count_tags
from collections import Counter 
import numpy as np 
import string 


MODEL = spacy.load('en_core_web_sm')
PUNCTUATION = string.punctuation + "..." + '(' + ')'

path_to_pred_dir = "/Users/talita/Documents/PhD/tacl/analyse-predictions" 
path_to_file_with_predictions = '{0}/bestmodels_predictions.json'.format(path_to_pred_dir)
path_to_filtered_fillers = "../coreference/dev_set_with_filtered_fillers.json"

with open(path_to_file_with_predictions, "r") as json_in: 
     data = json.load(json_in)

def sublist(lst1, lst2):
   ls1 = [element for element in lst1 if element in lst2]
   ls2 = [element for element in lst2 if element in lst1]
   return ls1 == ls2

class RevisionInstance: 

    # revision_instance = data[key]
    def __init__(self, key, revision_instance, keys):
        self.revision_instance = revision_instance
        self.key = key 
        self.keys = keys 
        self.left_context = revision_instance["LeftContext"]
        self.predictions = [prediction.strip() for prediction in revision_instance["GPT+Finetuning+P-perplexityPred"]] 
        self.revised_after_insertion = revision_instance["revised_after_insertion"]
        self.reference_type = revision_instance["reference-type"]
    
    @property
    def revlength(self): 
        if self.reference_type == "bigram": 
            return 2 
        
        elif self.reference_type == "unigram": 
            return 1 
        else: 
            return 3 


    @property 
    def revised_untill_insertion(self): 
        if "revised_untill_insertion" in self.keys: 
           return self.revision_instance["revised_untill_insertion"]
        else: 
           return self.revision_instance["revised_until_insertion"]


def filter_tags(tagged_fillers, reference_type):
    # check the length 
    filtered_list = []
    tags_to_exclude_unigrams = [".", ",", "!", ":", ";", "$", ")", "(", "MD", "RBR", "VBZ",  "LS", "VBD", "VB", "VBG", "VBN", "WP", "UH", "XX", "-RRB-", "NFP", "IN", "WDT", "FW", ";", "-LRB-", "WRB", '""', '``', 'RB', 'VBP', 'CC', 'CD']
    words_to_exclude_unigrams = ["the", "a", "an"]
    if reference_type == "unigram": 
        for elem in tagged_fillers:
            if elem != []: 
               tag = elem[0][1]
               if tag not in tags_to_exclude_unigrams: 
                  if elem[0][0] not in words_to_exclude_unigrams: 
                     filtered_list.append(elem)
    elif reference_type == "bigram": 
        for elem in tagged_fillers: 
            if elem != []: 
                tags = [x[1] for x in elem]
                if len(tags) == 2: 
                    if tags[0] not in tags_to_exclude_unigrams and tags[1] not in tags_to_exclude_unigrams:
                        filtered_list.append(elem)
                else: 
                    if tags[0] not in tags_to_exclude_unigrams: 
                       filtered_list.append(elem)

    else: 
        for elem in tagged_fillers: 
            if elem != []: 
                tags = [x[1] for x in elem]
                if len(tags) == 3: 
                    if tags[0] not in tags_to_exclude_unigrams and tags[1] not in tags_to_exclude_unigrams and tags[2] not in tags_to_exclude_unigrams:
                        filtered_list.append(elem)
                else: 
                    if tags[0] not in tags_to_exclude_unigrams: 
                       filtered_list.append(elem)
               
    return filtered_list  


def tag_predictions(predictions, revised_untill_insertion, revised_after_insertion, rev_length): 
    tagged_predictions = []
    for filler in predictions: 
        sent_to_tag = revised_untill_insertion + " " +  filler + " " + revised_after_insertion
        tokenized_revised_with_filler = MODEL(sent_to_tag) 
        # tokenized 
        tokenized_sent = [token.text for token in tokenized_revised_with_filler]
        # pos_tags 
        tagged_sent = [[token.text, token.tag_] for token in tokenized_revised_with_filler]


        # tokenized revised unitll insertion 
        tokenized_rev_untill = [token.text for token in MODEL(revised_untill_insertion)]


        rev_untill_insertion = tokenized_sent[0:len(tokenized_rev_untill)]
   

        if rev_untill_insertion == [] and tokenized_sent[0] == ' ': 
            begin_index = 1 
            filler_tokenized = tokenized_sent[begin_index:begin_index+rev_length]
            if filler == " ".join(filler_tokenized): 
                tagged_predictions.append(tagged_sent[begin_index: begin_index+rev_length])
            else: 
                tagged_predictions.append([[token.text, token.tag_] for token in MODEL(filler)])
    
        else: 
            filler_tokenized = tokenized_sent[len(tokenized_rev_untill):len(tokenized_rev_untill)+rev_length]
            if filler == " ".join(filler_tokenized): 
                tagged_predictions.append(tagged_sent[len(tokenized_rev_untill):len(tokenized_rev_untill)+rev_length]) 
            else: 
                tagged_predictions.append([[token.text, token.tag_] for token in MODEL(filler)])       

    return tagged_predictions

def main(): 
    counter = 0 
    for key, _ in data.items():     
        revision_instance = RevisionInstance(key, data[key], data[key].keys())
        print(key) 
        tagged_predictions = tag_predictions(revision_instance.predictions, revision_instance.revised_untill_insertion, revision_instance.revised_after_insertion, revision_instance.revlength) 
        print(revision_instance.predictions)

        filtered = filter_tags(tagged_predictions, data[key]["reference-type"])  
        
        
        fillers_to_return = []
        for filler in filtered: 
            filler_tokens =  " ".join([elem[0] for elem in filler])
            fillers_to_return.append(filler_tokens)

        fillers_to_return_new = [filler for filler in fillers_to_return if filler not in string.punctuation]

        print(fillers_to_return_new) 
main() 