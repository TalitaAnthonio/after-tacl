# script used to check whether a filler occurs in the coreference chain or not. 

import json 
import pdb
from typing import Type 
from collections import Counter

PATH_TO_FILE = "dev_with_coref_for_fillers.json"  


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
        freq_dict[dict_with_corefs[filler]] +=1 
        d[dict_with_corefs[filler]] = filler 
        

    freq_dict = dict(freq_dict)
    merged = {}
    print(freq_dict)
    for key, _ in freq_dict.items(): 
        filler_name = d[key]
        merged[filler_name] = {"counter": freq_dict[key], "coref": key}
    print(merged)


           



def main(): 
    data, num_to_check = read_json_lines(PATH_TO_FILE)
    print(num_to_check)
    print(len(data.keys()))



    for key, value in data.items(): 
        dict_with_coreferenced_fillers = {}
        fillers = [key for key  in data[key].keys() if key != "id"]
        for filler in fillers: 
            # the filler 
            
            
            references = check_if_filler_occurs_in_coref(filler, data[key][filler]["coref"], len(data[key][filler]["sents"]))
            # remove the filler from the list 
        
            if references != None: 
               print(references)
               # in case that the list of references is the same referring expression. 
               if len(list(set(references))) != 1: 
                  references = [reference for reference in references if reference != filler]
               dict_with_coreferenced_fillers[filler] = " ".join(sorted(references))
        print(dict_with_coreferenced_fillers)
        print("===================================")
        break 

main() 