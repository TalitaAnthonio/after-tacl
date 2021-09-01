import json 

with open("filtered_set_train_articles_tokenized_context_latest.json", "r") as json_in: 
     data = json.load(json_in)


counter = 0 
for key, _ in data.items(): 
    print("==============={0}=================".format(key))

    counter +=1 
    
    print("left")
    for elem in data[key]["BaseArticle"]["left_context"]: 
        print(elem)
     
    print("current")
    for elem in data[key]["BaseArticle"]["current_line"]: 
        print(elem)

    print("right")
    for elem in data[key]["BaseArticle"]["right_context"]: 
        print(elem)
    print("--------new------")
    
    print("left")
    for elem in data[key]["Tokenized_article"]["left"]: 
        print(elem)
    
    print("current")
    for elem in data[key]["Tokenized_article"]["current"]: 
        print(elem)

    print("right")
    for elem in data[key]["Tokenized_article"]["right"]: 
        print(elem)

    print("=============================")

    if counter == 30: 
       break 