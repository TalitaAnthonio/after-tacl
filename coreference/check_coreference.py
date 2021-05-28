import json 
import pdb
from typing import Type 
from collections import Counter
import numpy as np 

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

def main(): 
    data, num_to_check = read_json_lines(PATH_TO_FILE)
    avg_coref_chain = []
    for key, _ in data.items(): 
        fillers_with_coref = [filler for filler in data[key].keys() if filler != "id"]
        # Step 1: only take the fillers that we decided to keep 
        specific_fillers = file_with_specific_fillers[key]["filtered_fillers"]
        # Step 2: check whether the filler occured in the context or not according to the coreference chain 
        
        total_fillers_in_coref_chain = 0 
        for filler in specific_fillers: 

            # check if the key occurs in the dictionary 
            if filler in fillers_with_coref: 
                references = check_if_filler_occurs_in_coref(filler, data[key][filler]["coref"], len(data[key][filler]["sents"]))
                print("filler", filler, references)
                if references != None: 
                   total_fillers_in_coref_chain +=1 
        avg_coref_chain.append(total_fillers_in_coref_chain) 

                   
        
        print("====================")

    print("average with a coreference chain", np.mean(avg_coref_chain))

main()