import json 
from tools import SentenceSplitter, get_matching_sent_context
import pdb 
import re 

sentence_splitter = SentenceSplitter(use_sent=True)

with open("filtered_set_train_articles.json", "r") as json_in: 
     data = json.load(json_in)


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
    


def main(): 
    counter = 0 
    for key, _ in data.items(): 
        
        revision_instance = RevisionInstance(data[key])
                    
        left_context = revision_instance.left_context_splitted
        current = revision_instance.current_line_splitted
        right_context = revision_instance.right_context_splitted


        formatted = []
        for i in range(len(left_context)): 
            formatted = left_context
            if left_context[i].startswith('#'): 
                pattern = re.findall(r"[0-9]+.$", left_context[i])
                if pattern != []: 
                # remove the number from the line 
                    formatted[i] = re.sub(r'[0-9]+.$', r'', left_context[i])
                    formatted[i+1] = " ".join(pattern) + " " + left_context[i+1]
                    if i < len(left_context): 
                        i += 1 

            else: 
                formatted.append(left_context[i])
                
            
        print(formatted)
        break 
        
        for elem in current: 
            print(elem)
        
        for elem in right_context: 
            pattern = re.findall(r"[0-9]+.$", elem)
            print(elem, "pattern", pattern)
        print("========================")

        #current_line_tokenized = revision_instance.current_line_splitted


        """
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
                current_sent = res["current"]
                after_sent = res["after_sent"]

                if before_sent != []: 
                print("left", left_context)
                print("before", before_sent)
                left_context = left_context.split('\n') + before_sent


                if after_sent != []: 
                
                right_context = after_sent + right_context


                par = left_context + current + right_context

                print(par)

            #else: 
            #    pdb.set_trace()
            #    par = left_context + current + right_context

            
            #print(par)

            
        """
  
main()