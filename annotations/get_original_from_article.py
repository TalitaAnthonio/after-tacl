import json 
import re 
import pdb 

PATH_TO_FILE = "../get-context/filtered_set_train_articles_tokenized_context_latest_with_context.json"


with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)

for key, _ in data.items(): 
    original_in_article = data[key]["Tokenized_article"]["current"]
 

    if "BaseSentence" not in data[key].keys(): 
               
        try: 
            original_sentence = data[key]["Base_Sentence"]
        except KeyError: 
            original_sentence = " ".join(data[key]["base_tokenized"])
                   
              
    else: 
        original_sentence = data[key]["BaseSentence"]
    
    print("old", original_sentence)
    starts_with_bullet_point = re.findall(r"^[0-9]+\.", original_in_article[0])
   
    if starts_with_bullet_point: 
       original_sentence = " ".join(starts_with_bullet_point) + " " + original_sentence
    
    elif original_in_article[0].startswith("* "): 
        original_sentence = "* " + original_sentence
    
    else: 
        original_sentence = original_sentence
    

    print(original_in_article)
    print("new", original_sentence)
    print("==================")