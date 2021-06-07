# Script to get all the entities mentioned in the context. 

import json 

path_to_file = "/Users/talita/Documents/PhD/tacl/data/references_for_lm.json"

path_to_other = "/Users/talita/Documents/PhD/corpora/rulebook_diffs/2019-09-23/boardgame_scripts/wikihow/data/unigrams/SingleInsertions_coreferenced.json"

with open(path_to_file, 'r') as json_in: 
     data = json.load(json_in)

with open(path_to_other, 'r') as json_in: 
     second_part = json.load(json_in)


def main(): 

    d = {}
    for key, _ in data.items(): 
        print(key)
        #corefs = data[key]['coref']
        #except KeyError: 
        #    pdb.set_trace()
        total_referring_expressions = 0 

        if "coref" in data[key].keys(): 
            corefs = data[key]['coref']
        else: 
            corefs = second_part[key]['coref']

        highest_num = 0 
        longest_chain = []
    

        all_expressions = []
        expressions_per_chain = []
        for coref_id, _ in corefs.items():
            referring_expressions = [' '.join(mention['ref']) for mention in corefs[coref_id]['mentions']]
            expressions_per_chain.append(referring_expressions)
            all_expressions.extend(referring_expressions)
        

        
        print(all_expressions)
        unique_references_in_context = list(set(all_expressions))
        all_references_in_context = expressions_per_chain

        d[key] = {"unique_references_in_context": unique_references_in_context, "all_references_in_context": expressions_per_chain}

        with open("dev_set_references.json", "w") as json_in: 
             json.dump(d, json_in)

        print("=======================================")

main()