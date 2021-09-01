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



        if "BaseSentence" not in instance[key].keys(): 
               
               try: 
                    original_sentence = data[key]["Base_Sentence"]
               except KeyError: 
                   original_sentence = " ".join(data[key]["base_tokenized"])
                   
              
        else: 
            original_sentence = data[key]["BaseSentence"]

        self.original_sentence = original_sentence

        
    




def main(): 

    counter = 0 
    d = {}


    for key, _ in data.items(): 
        revision_object = RevisionInstance(data, key)
        original_sentence = revision_object.original_sentence


        if revision_object.left_paragraph: 
            title = revision_object.left_paragraph[0] 
                    
            previous_two_sentences = revision_object.left_paragraph[-2:]

              
            try: 
                if previous_two_sentences[0] == title: 
                    print(previous_two_sentences[0], "equal to title")
                    previous_two_sentences = revision_object.left_paragraph[-1:]
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
   
           scenario = "SCENARIO 1"

           if revision_object.right_context_splitted: 
               next_sentence = [revision_object.right_context_splitted[0]]
           else: 
               next_sentence = []

           print("full paragraph")
           print(revision_object.full_paragraph)

           print("subset")
           part_from_context = [title] + something_in_between + previous_two_sentences + [original_sentence] + next_sentence
           print(part_from_context)
           print("original", original_sentence)
           #print("left", revision_object.left_paragraph)


           #print("========================")
        
        """
        else: 
            index_of_current = data[key]["index_of_sentence_in_context"]

            # SCENARIO 2: there are only sentences after the current line on the line. 
            scenario = "SCENARIO 2"
            if index_of_current == 0: 
               print("scenario 2")

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


            # SCENARIO 3: there are only sentences before the current line 

            elif index_of_current == (len(sentence_splitter.tokenize(revision_object.current_line)) - 1): 

                print("scenario 3")
                scenario = "SCENARIO 3"
                previous_sentence_first = [sentence_splitter.tokenize(revision_object.current_line)[index_of_current-1]]
               
                 

                if (index_of_current-2) in [i for i in range(len(sentence_splitter.tokenize(revision_object.current_line)))]:  
                    previous_sentence_second = [sentence_splitter.tokenize(revision_object.current_line)[index_of_current-2]]
                else: 
                    if revision_object.left_paragraph: 

                        previous_sentence_second = [revision_object.left_context_splitted[-2]]
                    else: 
                        previous_sentence_second = []
            


                if revision_object.right_paragraph: 
                    next_sentence = [revision_object.right_paragraph[0]]

                else: 
                    next_sentence = []

                
                part_from_context = [title] + something_in_between + previous_sentence_second + previous_sentence_first  +  [original_sentence] + next_sentence 


                
            # SCENARIO: there are sentences before and after 
            else: 
                # the sentence before
                print("scenario final") 
                scenario = "SCENARIO 4"
                previous_sentence_first = [sentence_splitter.tokenize(revision_object.current_line)[index_of_current-1]]

                try: 
                    previous_sentence_second = [sentence_splitter.tokenize(revision_object.current_line)[index_of_current-2]]

                except IndexError: 
                    if revision_object.left_context: 
                        previous_sentence_second = [revision_object.left_context[-1]]
                    else: 
                        previous_sentence_second = []
                

                next_sentence = [sentence_splitter.tokenize(revision_object.current_line)[index_of_current+1]]

                
                part_from_context = [title] + something_in_between + previous_sentence_first + previous_sentence_second +  [original_sentence] + next_sentence 



        d[key] = data[key]
        d[key].update({"FullParagraph": revision_object.full_paragraph, "ContextForAnnotation": part_from_context, "Scenario": scenario})


    with open("train_set_with_context_subset.json", "w") as json_out: 
            json.dump(d, json_out)

    """
    
main()  