import json 
from tools import SentenceSplitter

sentence_splitter = SentenceSplitter(use_sent=True)

with open("filtered_set_train_articles.json", "r") as json_in: 
     data = json.load(json_in)


counter = 0 
for key, _ in data.items(): 
    print(data[key]["BaseArticle"].keys())
    
    left_context_splitted = sentence_splitter.tokenize([sent for sent in data[key]["BaseArticle"]["left_context"] if "Timestamp" not in sent])
    current_line_splitted = sentence_splitter.tokenize([sent for sent in data[key]["BaseArticle"]["current_line"] if "Timestamp" not in sent])
    right_context_splitted = sentence_splitter.tokenize([sent for sent in data[key]["BaseArticle"]["right_context"] if "Timestamp" not in sent])

    print("=========================================")

    print("before")
    print(data[key]["BaseArticle"]["current_line"])

    print("\n")
    print("after")
    for elem in current_line_splitted: 
        print(elem)

    counter +=1 

    if counter == 20: 
       break 