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

        # the sentence_tokenized_components 
        self.left_context_splitted = instance[key]["Tokenized_article"]["left"]
        self.current_splitted = instance[key]["Tokenized_article"]["current"]
        self.right_context_splitted = instance[key]["Tokenized_article"]["right"]


        # types --> list 
        self.right_paragraph = make_paragraph_right(instance[key]["Tokenized_article"]["right"])
        self.left_paragraph = make_paragraph_left(instance[key]["Tokenized_article"]["left"])


        self.full_paragraph = self.left_paragraph + self.current_splitted + self.right_paragraph


def extract_subset(current_line, current_line_splitted, index_of_original): 
    # if there are several sentences on the same line, take them (up to two)

    # "We said the previous (up to) 2 sentences (if there are previous sentences on the same line)"

    current_line_splitted = sentence_splitter.tokenize(current_line) 

    #if len(current_line_splitted) 


    print(current_line_splitted)
    
    print("==============================")
    


        





def main(): 

    counter = 0 
    for key, _ in data.items(): 
        revision_object = RevisionInstance(data, key)

        if "BaseSentence" not in data[key].keys(): 
               
               #TODO: solve this problem 
               try: 
                    original_sentence = data[key]["Base_Sentence"]
               except KeyError: 
                   original_sentence = " ".join(data[key]["base_tokenized"])
                   
              
        else: 
            original_sentence = data[key]["BaseSentence"]
        print("======================================")


        if revision_object.left_paragraph: 
            title = revision_object.left_paragraph[0] 
                    
            previous_two_sentences = revision_object.left_context_splitted[-2:]

              
            try: 
                if previous_two_sentences[-3] == title: 
                    something_in_between = []
                else: 
                    something_in_between = ["(...)"]
            except IndexError: 
                  something_in_between = ["(...)"]

            

        else: 
            title = ""
            previous_two_sentences = []
  


        # SCENARIO 1: there are no sentences on the same line 

        if len(sentence_splitter.tokenize(revision_object.current_line)) == 1:
   
            

           if revision_object.right_context_splitted: 
               next_sentence = [revision_object.right_context_splitted[0]]
           else: 
               next_sentence = []

           print("full paragraph")
           print(revision_object.full_paragraph)

           print("subset")
           part_from_context = [title] + something_in_between + previous_two_sentences + [original_sentence] + next_sentence
           print(part_from_context)
           print(original_sentence)
        
        else: 
            index_of_current = data[key]["index_of_sentence_in_context"]


            # there are sentences before the current line 
            #pdb.set_trace()


         

            # there are sentences before and after the current line 

            # SCENARIO 2: there are only sentences after the current line on the line. 
            if index_of_current == 0: 

               # If there is just one sentence after the original sentence on the current line, then take that one. 
               # If there are two sentences after the original sentence on the current line, then take those two. 
               next_sentence_first = [sentence_splitter.tokenize(revision_object.current_line)[1]]
               if len(sentence_splitter.tokenize(revision_object.current_line)) >= 3: 
                  next_sentence_second = [sentence_splitter.tokenize(revision_object.current_line)[2]]
               else: 
                   next_sentence_second = []
               

               part_from_context = [title] + something_in_between + previous_two_sentences + [original_sentence] + next_sentence_first + next_sentence_second
               
               print("subset new")
               print(part_from_context)
               print(original_sentence)


                


               # take the previous two sentences from the left context 







main() 