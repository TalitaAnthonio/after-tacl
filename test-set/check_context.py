import json 

PathToContext = "../get-context/filtered_set_test_articles_tokenized_context_latest_with_context.json" 

with open(PathToContext, "r") as json_in: 
     data = json.load(json_in)


for key, _ in data.items(): 
    print(data[key].keys())
    print(data[key]['ContextBefore'])
    print(data[key]['ContextAfter'])
    break 