# used to correct the remaining errors from the sentence splitter. 


import json

from nltk.util import Index 
from tools import SentenceSplitter, get_matching_sent_context
import pdb 
import re 

sentence_splitter = SentenceSplitter(use_sent=True)

with open("filtered_set_train_articles.json", "r") as json_in: 
     data = json.load(json_in)

def format_current(x): 
    """
        if you have something like this "5 ." then merge it back to "5 ."
    """
    replaced = [re.sub(r'^([0-9]+)\s', r"\1", elem) for elem in x]
    return replaced 

def make_paragraphs(left_context_splitted): 
    """
        Function used to make paragraphs from the base sentence to up: 
        Arg: left_context_splitted 
    """
    before_sent = [elem.strip() for elem in left_context_splitted]
    before_sent.reverse()

    
    paragraph_reverse = []
    for sentence in before_sent: 
        if sentence.startswith("#"): 
            index = before_sent.index(sentence)
            paragraph_reverse = before_sent[:index+1]
            break 
    paragraph_reverse.reverse()
    par =  ' '.join([elem + '\n' for elem in paragraph_reverse])
    return par 

class RevisionInstance: 

    def __init__(self, instance): 
        self.instance = instance
        self.left_context_splitted =  sentence_splitter.tokenize([sent for sent in self.instance["BaseArticle"]["left_context"] if "Timestamp" not in sent])
        self.current_line_splitted = sentence_splitter.tokenize([sent for sent in self.instance["BaseArticle"]["current_line"] if "Timestamp" not in sent])
        self.right_context_splitted = sentence_splitter.tokenize([sent for sent in self.instance["BaseArticle"]["right_context"] if "Timestamp" not in sent])
    


def correct_splitter(context): 
    """
        Hier zit een fout in. 
    """

    # correct the problem with remaining *.
    formatted = []
    for i in range(len(context)): 
        formatted = context
        if context[i].startswith('#'): 
            pattern = re.findall(r"[0-9]+.$", context[i])
            if pattern != [] and i != len(context)-1: 
            # remove the number from the line 
                formatted[i] = re.sub(r'[0-9]+.$', r'', context[i])
                formatted[i+1] = " ".join(pattern) + " " + context[i+1]
                if i < len(context): 
                    i += 1 

        else: 
            formatted[i] = context[i]
    
    # fix the remaining problem with the stars 
    context_new = []
    for sent in formatted: 
    
        if " * " in sent: 
            sent = sent.replace(" *", "\n*")
            context_new.extend(sent.split("\n"))
            
        else: 
            context_new.append(sent)

    return context_new



new_dict = {}

def main(): 
    counter = 0 
    d = {}
    for key, _ in data.items(): 

        
        d[key] = data[key]

        revision_instance = RevisionInstance(data[key])

        # correct remaining errors with the splitter    
        # type is a list 
          
        left_context = correct_splitter(revision_instance.left_context_splitted)
        
        current_line_tokenized = revision_instance.current_line_splitted
    
        right_context = correct_splitter(revision_instance.right_context_splitted) 


        
        if len(current_line_tokenized) > 1: 
            print("===========================")
            counter +=1 
            print(counter)

            print(key)
            print(current_line_tokenized)
        
    

            if "Base_Sentence" not in data[key].keys():
                original_sentence = " ".join(data[key]["base_tokenized"])
            else: 
                original_sentence =  data[key]["Base_Sentence"]
            
        
            res = get_matching_sent_context(current_line_tokenized, original_sentence)
            
            before_sent = res["before_sent"]
            current_sent = format_current(res["current"])
            after_sent = res["after_sent"]

            if before_sent != []: 
                print("left", left_context)
                print("before", before_sent)
                left_context = left_context + before_sent
                
        


            if after_sent != []: 
                

                right_context = after_sent + right_context

            
            d[key].update({"Tokenized_article": {"left": left_context, "current": current_sent, "right": right_context}})
            #  "match_found": "no", 
            #"index_of_sentence_in_context": index_of_max_bleu
            d[key].update({"match_found": res["match_found"], 
            "index_of_sentence_in_context": res["index_of_sentence_in_context"]})


            #par = left_context + current_sent + right_context
            
        else:
            d[key].update({"Tokenized_article": {"left": left_context, "current": current_line_tokenized, "right": right_context}}) 
 
        #print(par)


        #with open("filtered_set_train_articles_tokenized_context_latest.json", "w") as json_out: 
        #    json.dump(d, json_out)     

        
main()