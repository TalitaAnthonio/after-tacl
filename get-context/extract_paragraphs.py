# TODO: extract paragraphs 
# TODO: extract the algorithms 

import pdb 


import json
from logging import currentframe 
import re

from nltk.util import Index
from numpy import index_exp 
from tools import SentenceSplitter, correct_splitter

PATH_TO_FILE = "filtered_set_train_articles_tokenized_context_latest.json"

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)



sentence_splitter = SentenceSplitter(use_sent=True)


def make_paragraph_left(left_context): 

    """

        Make paragraphs for left context. 
        left_context {list} : list with sentences  
    """ 

    paragraph_reverse = []
    left_context.reverse()
    for sentence in left_context: 
        if sentence.startswith("#"): 
            index = left_context.index(sentence)
            paragraph_reverse = left_context[:index+1]
            break 
    paragraph_reverse.reverse()
    return paragraph_reverse

def make_paragraph_right(right_context): 
    """
        Make paragraphs for right context 

        right_context {list}: list with sentences 
    """
    right_context_paragraph = []
    for index, sentence in enumerate(right_context,0): 

        # if the sentence does not 
        if sentence.startswith('#'): 
           break 
        else: 
            right_context_paragraph.append(sentence)

    return right_context_paragraph
    
def format_current(x): 
    replaced = re.sub(r'^([0-9]+)\s', r"\1", x)
    return replaced 

class RevisionInstance: 

    def __init__(self, instance, key): 
        
        self.left_context = instance[key]["BaseArticle"]["left_context"]
        self.current_line = instance[key]["BaseArticle"]["current_line"]
        self.right_context = instance[key]["BaseArticle"]["right_context"]
        self.current_line_raw_splitted = sentence_splitter.tokenize([sent for sent in instance[key]["BaseArticle"]["current_line"] if "Timestamp" not in sent])

        # the sentence_tokenized_components 
        self.left_context_splitted = instance[key]["Tokenized_article"]["left"]
        self.original_in_article = instance[key]["Tokenized_article"]["current"]
        self.right_context_splitted = instance[key]["Tokenized_article"]["right"]


        # types --> list 
        self.right_paragraph = make_paragraph_right(instance[key]["Tokenized_article"]["right"])
        self.left_paragraph = make_paragraph_left(instance[key]["Tokenized_article"]["left"])


        self.full_paragraph = self.left_paragraph + self.original_in_article + self.right_paragraph

        if self.left_paragraph: 
            self.title = [self.left_paragraph[0]] 
        else: 
            self.title = []

        if "BaseSentence" not in instance[key].keys(): 
               
               try: 
                    original_sentence = data[key]["Base_Sentence"]
               except KeyError: 
                   original_sentence = " ".join(data[key]["base_tokenized"])
                   
              
        else: 
            original_sentence = data[key]["BaseSentence"]

        self.original_sentence = original_sentence


        if "index_of_sentence_in_context" in instance[key].keys(): 
            self.index = data[key]["index_of_sentence_in_context"]
        else: 
            self.index = []
    
def format_original_sentence(original_sentence, original_sentence_splitted): 
    #assert len(original_sentence_splitted) == 1
    starts_with_number = re.findall(r"^[0-9]+.", " ".join(original_sentence_splitted))
    if starts_with_number: 
        #print(original_sentence)
        #print(original_sentence_splitted)
        original_sentence_new =  " ".join(starts_with_number) + " " +  original_sentence
        #print(original_sentence_new)


    else: 
          starts_with_bullet = re.findall(r"^\*", " ".join(original_sentence_splitted))
          if starts_with_bullet: 
            #print(original_sentence)
            #print(original_sentence_splitted)
            original_sentence_new =  " ".join(starts_with_bullet) + " " +  original_sentence
            #print(original_sentence_new)
          else: 
              original_sentence_new = original_sentence
    return original_sentence_new

def get_right_context(current_line_splitted, right_context_splitted, index_of_sentence): 

    # if there are no other lines on current_line_splitted 
    if index_of_sentence == []: 
       if right_context_splitted: 
          context_after = right_context_splitted[0]
       else: 
          context_after = []
    else: 
        # if the original sentence is the last one on the line 
        # then take the first sentence of the right context 
        if index_of_sentence == len(current_line_splitted)-1: 
           if right_context_splitted: 
              context_after = right_context_splitted[0] 
           else: 
              context_after = []
        else: 
            context_after = current_line_splitted[index_of_sentence+1]
           
    return context_after

def main(): 

    counter = 0 
    d = {}


    for key, _ in data.items(): 
       
        revision_object = RevisionInstance(data, key)
        original_sentence_raw = revision_object.original_sentence
        original_sentence_in_article = revision_object.original_in_article
        original_sentence = format_original_sentence(original_sentence_raw, original_sentence_in_article)
        title = revision_object.title
        context_after = get_right_context(revision_object.current_line_raw_splitted, revision_object.right_context_splitted, revision_object.index)
        
        print("============================")
        print(original_sentence) 
        print(revision_object.current_line_raw_splitted)
        
        if revision_object.index == [] or revision_object.index == 0: 
           print("there are no sentences before on the same line.")
        
        else: 
            
            if revision_object.index == 1: 
               sentence_before = revision_object.left_context_splitted[-1]
               print("there is just a sentence before")
            
            # there are two sentences on the same line 
            elif revision_object.index == 2: 
               sentence_before = revision_object.current_line_raw_splitted[1]
               sentence_before_preceding = revision_object.current_line_raw_splitted[0]

               # if the sentence before preceding is the title, then only use the title 
               if sentence_before_preceding == revision_object.title:
                  context_before = revision_object.title + sentence_before
               else: 
                  context_before = revision_object.title + ["(...)"] + [sentence_before_preceding] + [sentence_before] 

               print("========= full par ======")
               for elem in revision_object.full_paragraph: 
                   print(elem)
               

               print("subset")
               print(context_before)
               print(original_sentence_raw)
               print(context_after)
            
                  

            
            else: 
                print("there are no preceding sentences")

        



    
main()  