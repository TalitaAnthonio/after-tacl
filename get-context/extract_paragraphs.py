# TODO: extract paragraphs 
# TODO: extract the algorithms 


import json 

PATH_TO_FILE = "filtered_set_train_articles_tokenized_context.json"

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)


class RevisionInstance: 

    def __init__(self, instance, key): 
        
        self.left_context = instance[key]["BaseArticle"]["left_context"]
        self.current_line = instance[key]["BaseArticle"]["current_line"]
        self.right_context = instance[key]["BaseArticle"]["right_context"]

        self.left_context_splitted = instance[key]["Tokenized_article"]["left"]
        self.current_splitted = instance[key]["Tokenized_article"]["current"]
        self.right_context_splitted = instance[key]["Tokenized_article"]["right"]


        # types --> list 
        self.right_paragraph = make_paragraph_right(instance[key]["Tokenized_article"]["right"])
        self.left_paragraph = make_paragraph_left(instance[key]["Tokenized_article"]["left"])


        self.full_paragraph = [self.left_paragraph if self.left_paragraph else "EMPTY"] +  ["REVISED"] + self.current_splitted + self.right_paragraph


        


def make_paragraph_left(left_context): 

    """

        Make paragraphs for left context. 
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
    """
    right_context_paragraph = []
    for index, sentence in enumerate(right_context,0): 

        # if the sentence does not 
        if sentence.startswith('#'): 
           break 
        else: 
            right_context_paragraph.append(sentence)

    return right_context_paragraph
    



def main(): 

    counter = 0 
    for key, _ in data.items(): 
        revision_object = RevisionInstance(data, key)
        
        
        print(revision_object.full_paragraph) 
        print(data[key]["RevisedSentence"])
        print("============================")


main() 