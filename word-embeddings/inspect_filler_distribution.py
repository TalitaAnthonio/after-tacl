import json 

with open("dev_set_references.json", "r") as json_in: 
     references = json.load(json_in)
    
with open("../coreference/filtered_predictions_step2.json", "r") as json_in: 
     file_with_pred = json.load(json_in)

with open("/Users/talita/Documents/PhD/tacl/baselines/recency_dev.json", "r") as json_in: 
     file_with_recency = json.load(json_in)

for key, _ in file_with_pred.items(): 
    print(key)
    print(file_with_pred[key]["revised_sentence"])
    predictions = file_with_pred[key]["filtered2"]
    references_from_coref = references[key]["unique_references_in_context"]
    print(predictions)

    print("recency .... ")
    if key in file_with_recency.keys(): 
       references_rec = list(set(file_with_recency[key]))
    else: 
        references_rec = list(set(references_from_coref))
    
    print("references", references_rec)
    
    filtered_references = []
    for reference in references_rec: 
        if reference.lower() not in [prediction.lower() for prediction in predictions]: 
           filtered_references.append(reference)
    
    print(filtered_references)
           

    print("=============================")
