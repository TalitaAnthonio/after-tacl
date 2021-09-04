import json 
import pdb 


with open("filtered_train_preds_final_nouns_only_new.json", "r") as json_in: 
        data = json.load(json_in)

def filter_second_step(filtered_fillers): 
    d = {}

    for elem in filtered_fillers: 
        if len(elem.split()) == 2: 
            noun = elem.split()[1]
        elif len(elem.split()) == 3: 
            noun = elem.split()[2]
        else: 
            noun = elem 
        if noun in d.keys(): 
            d[noun].append(elem) 
        else: 
            d[noun] = []
            d[noun].append(elem)

    return d 


d = {}
for key, _ in data.items(): 
    filtered_fillers = data[key]["filtered_fillers"]
    print("before", filtered_fillers)
    print(data[key].keys())
    filtered = filter_second_step(filtered_fillers)
    reference = data[key]["reference"]

    if type(reference) == list:
       reference = " ".join(reference)
    

    fillers_to_keep = []
    for noun, _ in filtered.items(): 
        if noun not in ["the", "a", "to"]: 
            if reference.lower() in filtered[noun]: 
                fillers_to_keep.append(reference.lower())
            else: 
                fillers_to_keep.append(filtered[noun][0])

    d[key] = data[key]
    d[key].update({"filtered_fillers2": fillers_to_keep})

with open("filtered_train_preds_final_nouns_only_new_v2.json", "w") as json_out: 
     json.dump(d, json_out)
