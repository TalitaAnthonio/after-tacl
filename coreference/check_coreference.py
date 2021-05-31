import json 
import pdb
from typing import Type 
from collections import Counter
import numpy as np 

path_to_pred_dir = "/Users/talita/Documents/PhD/tacl/analyse-predictions" 
path_to_file_with_predictions = '{0}/bestmodels_predictions.json'.format(path_to_pred_dir)

with open(path_to_file_with_predictions, "r") as json_in: 
     file_with_predictions = json.load(json_in)

PATH_TO_FILE = "dev_with_coref_for_fillers.json"  
PATH_TO_FILTERED_SET = "dev_set_with_filtered_fillers.json"




def read_json_lines(path_to_json_lines):
    d = {} 
    num_to_check = 0 
    with open(path_to_json_lines) as json_lines_file: 
         for line in json_lines_file: 
             #print(line) 
             line = json.loads(line)
             try: 
                d[line['id']] = line
             except TypeError: 
                 num_to_check += 1 
    return d, num_to_check 


with open(PATH_TO_FILTERED_SET, "r") as json_in: 
     file_with_specific_fillers = json.load(json_in)


def check_if_filler_occurs_in_coref(filler, coref_chains, sentence_length): 
    # iterate through {0: {"ref":, "mentions"}}
    if type(coref_chains) == str: 
       return None 
    else: 
        for key, _ in coref_chains.items(): 
            mentions = coref_chains[key]["mentions"]
            sentence_indexes = [mention["sentenceIndex"] for mention in mentions]
            references = [" ".join(mention["ref"]) for mention in mentions]
            if sentence_length-1 in sentence_indexes: 
                if filler in references: 
                    return references
                    break 
                break 


def check_if_corefs_are_same(dict_with_corefs): 
    # dict that counts the lists: 
    # Counter({'The steak the Steak': 1, 'the steaks the steaks the steaks the steaks': 1, 'the meat the meat': 1, 'the beef the beef': 1, 'The steak the Steak the steak the steak the steak the steak the steak': 1, 'your grill your grill your prepared grill': 1}
    freq_dict = Counter()
    d = {}
    for filler, _ in dict_with_corefs.items(): 
        freq_dict[" ".join(dict_with_corefs[filler])] +=1 
        d[" ".join(dict_with_corefs[filler])] = filler 
        

    freq_dict = dict(freq_dict)
    merged = {}
    print(freq_dict)
    for key, _ in freq_dict.items(): 
        filler_name = d[key]
        merged[filler_name] = {"counter": freq_dict[key], "coref": key}
    return merged 


def main(): 
    data, num_to_check = read_json_lines(PATH_TO_FILE)
    avg_coref_chain = []
    avg_len = []
    for key, _ in data.items(): 
        coref_dict_per_filler = {}
        
        print("===============================================")

        # remember that these are all the fillers 
        fillers_with_coref = [filler for filler in data[key].keys() if filler != "id"]
        # Step 1: only take the fillers that we decided to keep 
        specific_fillers = file_with_specific_fillers[key]["filtered_fillers"]

        print("first fillers", specific_fillers)
        print(file_with_predictions[key]["RevisedSentence"])

        # Step 2: check whether the filler occured in the context or not according to the coreference chain 
        
        total_fillers_in_coref_chain = 0 
        for filler in specific_fillers: 

            # check if the key occurs in the dictionary 
            if filler in fillers_with_coref: 
                correct_filler  = file_with_predictions[key]["CorrectReference"]
                references = check_if_filler_occurs_in_coref(filler, data[key][filler]["coref"], len(data[key][filler]["sents"]))
                if references != None: 
                    coref_dict_per_filler[filler] = sorted([reference for reference in references if reference != correct_filler])
        
        merged = check_if_corefs_are_same(coref_dict_per_filler)
        fillers_in_same_coref_chain = []
        for key, _ in merged.items(): 
            if merged[key]["counter"] > 1: 
                references = merged[key]["coref"] 
                for filler, references in coref_dict_per_filler.items(): 
                    if " ".join(coref_dict_per_filler[filler]) == " ".join(references): 
                        fillers_in_same_coref_chain.append(filler)
        

        final_selected_fillers = [filler for filler in specific_fillers if filler not in fillers_in_same_coref_chain]
        print("final selected fillers", final_selected_fillers)
        avg_len.append(len(final_selected_fillers))
        
    print(np.mean(avg_len))
main()