import numpy as np 
import json 
import pdb 
import spacy 

# dict_keys(['coref', 'sents', 'filename', 'base_tokenized', 'id', 'revised_tokenized', 'revised_sentence', 
# 'insertion_phrases', 'Base_Sentence', 'Base_Nr', 'Revised_Nr', 'parsed_revised_sentence', 'Base_Article', 
# 'Base_Article_Clean', 'par', 'index_of_insertion', 'index_of_reference', 'bigram', 'stats', 'insertion', 
# 'reference', 'reference-type', 'position-of-ref-in-insertion', 'Split', 'insertion-type', 
# 'language_model_text', 'revised_afer_insertion', 'revised_untill_insertion'])


USE_REV_ONLY = False

nlp = spacy.load("en_core_web_sm")



with open("../../tacl/data/references_for_lm.json", "r") as json_in: 
     all_data = json.load(json_in)


def count_vocabulary(sentences): 
    tokens = []
    for sent in sentences: 
        for token in sent: 
            tokens.append(token) 
    
    print("total tokens", len(tokens)) 
    print("vocab size", len(list(set(tokens)) ))


def tokenize(string): 
    tokenized = nlp(string)
    return [token.text for token in tokenized]

def format_pars(par):
    pars = [tokenize(sent) for sent in par.strip().split('\n') if "# Timestamp" not in sent]
    tokenized_pars = []
    for sent in pars: 
        for token in sent: 
            tokenized_pars.append(token)
    
    return tokenized_pars

def count_vocabulary_par(pars, sentences): 
    pass 



def main(): 
    sent_lengths = []
    sentences = []
    pars = []
    for key, _ in all_data.items(): 
       
        try: 
            rev_sent = all_data[key]["revised_tokenized"]
        except KeyError: 
            assert type(all_data[key]["revised_sentence"]) == list
            rev_sent = all_data[key]["revised_sentence"]

            sent_lengths.append(len(rev_sent))
            sentences.append(rev_sent)
            pars.append(all_data[key]["par"])
        

    if USE_REV_ONLY: 
        print("the average sentence length is", np.mean(sent_lengths))
        count_vocabulary(sentences)
    
    else: 

        texts_with_pars = []
        texts_with_pars_len = []
        sents_per_pars = []
        sents_per_pars_len = []

        sentence_lengths = []
        for par, revised_sent in zip(pars, sentences):
            tokenized_par = format_pars(par)
            complete_text = tokenized_par + revised_sent
            texts_with_pars.extend(complete_text)
            #print(len(complete_text))
            sents_per_pars_len.append(len(complete_text))

            # average words per par 
            #print(texts_with_pars)
            #print(len(texts_with_pars))
            #sents_per_pars_len.append(len(texts_with_pars))
            
            sents_per_pars_len.extend([len(tokenize(sent)) for sent in par.strip().split('\n') if "# Timestamp" not in sent])
            sents_per_pars_len.append(len(revised_sent))
            
            #sents_per_pars_len.append(len(revised_sent))
            #print(sents_per_pars_len)
            #print([tokenize(sent) for sent in par.strip().split('\n') if "# Timestamp" not in sent])

            #texts_with_pars_len.append(len(complete_text))
        #count_vocabulary_par(pars, sentences)

        avg_text_length = np.mean(texts_with_pars_len)
        token_size = len(texts_with_pars)
        vocab_size = len(list(set(texts_with_pars)))

        print("avg_text_length", avg_text_length)
        print("token size", token_size)
        print("vocab size", vocab_size)
        print("avg. words in par", np.mean(sents_per_pars_len))
main()
