import json 

with open("filtered_set_train_articles_tokenized_context_latest.json", "r") as json_in: 
     data = json.load(json_in)


counter = 0 
for key, _ in data.items(): 

    counter +=1 
    
    
    print(data[key]["BaseArticle"]["left_context"])
    print(data[key]["BaseArticle"]["current_line"])
    print(data[key]["BaseArticle"]["right_context"])
    print("--------new------")
    print(data[key]["Tokenized_article"]["left"])
    print(data[key]["Tokenized_article"]["current"])
    print(data[key]["Tokenized_article"]["right"])

    print("=============================")

    if counter == 30: 
       break 