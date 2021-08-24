import json 
from tools import SentenceSplitter, get_matching_sent_context
import pdb 
import re 

sentence_splitter = SentenceSplitter(use_sent=True)

with open("filtered_set_train_articles.json", "r") as json_in: 
     data = json.load(json_in)

def normalize_punkt(text):
    """replace unicode punctuation by ascii"""
    text = re.sub('[\u2010\u2043]', '-', text)  # hyphen
    text = re.sub('[\u2018\u2019]', "'", text)  # single quotes
    text = re.sub('[\u201c\u201d]', '"', text)  # double quotes
    return text


def format_new(string): 
    line = normalize_punkt(string)
    line = re.sub(r'<.*?>', r'', string)
    line = re.sub(r'\[\[Image:.*?\]\]', r'', line)
    line = line.lstrip('-*\\0123456789. ')
    line = re.sub(r'\[ \[[^\[]*?\|(.*?)\] \]', r'\1', line)

    # apply to deal with isues caused by my sentence splitter 
    line = re.sub(r' .$', r'.', line )
    line = re.sub(r' ,', r',', line)
    return line 

def make_paragraphs(left_context_splitted): 
    """
        Function used to make paragraphs: 
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
        self.right_context_splitted = sentence_splitter.tokenize([sent for sent in self.instance["BaseArticle"]["right_context"] if "Timestamp" not in sent])
        self.current_line_splitted = sentence_splitter.tokenize([sent for sent in self.instance["BaseArticle"]["current_line"] if "Timestamp" not in sent])
    


def main(): 
    counter = 0 
    for key, _ in data.items(): 
        
        
      
        revision_instance = RevisionInstance(data[key])
        par = make_paragraphs(revision_instance.left_context_splitted)


        current_line_tokenized = revision_instance.current_line_splitted


 
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
            
            print(original_sentence)
            res = get_matching_sent_context(current_line_tokenized, original_sentence)

            print(res)


main()