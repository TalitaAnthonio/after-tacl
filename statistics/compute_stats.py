import numpy as np 
import json 
import pdb 

# dict_keys(['coref', 'sents', 'filename', 'base_tokenized', 'id', 'revised_tokenized', 'revised_sentence', 
# 'insertion_phrases', 'Base_Sentence', 'Base_Nr', 'Revised_Nr', 'parsed_revised_sentence', 'Base_Article', 
# 'Base_Article_Clean', 'par', 'index_of_insertion', 'index_of_reference', 'bigram', 'stats', 'insertion', 
# 'reference', 'reference-type', 'position-of-ref-in-insertion', 'Split', 'insertion-type', 
# 'language_model_text', 'revised_afer_insertion', 'revised_untill_insertion'])

with open("../../tacl/data/references_for_lm.json", "r") as json_in: 
     all_data = json.load(json_in)


def count_vocabulary(sentences): 
    tokens = []
    for sent in sentences: 
        for token in sent: 
            tokens.append(token) 
    
    print("total tokens", len(tokens)) 
    print("vocab size", len(list(set(tokens)) ))



def main(): 
    sent_lengths = []
    sentences = []
    for key, _ in all_data.items(): 
        try: 
            rev_sent = all_data[key]["revised_tokenized"]
        except KeyError: 
            assert type(all_data[key]["revised_sentence"]) == list
            rev_sent = all_data[key]["revised_sentence"]

        sent_lengths.append(len(rev_sent))
        sentences.append(rev_sent)
    
    print("the average sentence length is", np.mean(sent_lengths))
    count_vocabulary(sentences)

main()
