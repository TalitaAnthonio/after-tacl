import json 


path_to_pred_dir = "/Users/talita/Documents/PhD/tacl/analyse-predictions" 
path_to_file_with_predictions = '{0}/bestmodels_predictions.json'.format(path_to_pred_dir)
path_to_filtered_fillers = "../coreference/dev_set_with_filtered_fillers.json"

with open(path_to_file_with_predictions, "r") as json_in: 
     data = json.load(json_in)


with open(path_to_filtered_fillers, "r") as json_in: 
     filtered_fillers = json.load(json_in)


class RevisionInstance: 

    # revision_instance = data[key]
    def __init__(self, key, revision_instance, keys):
        self.revision_instance = revision_instance
        self.key = key 
        self.keys = keys 
        self.left_context = revision_instance["LeftContext"]
        self.predictions = [prediction.strip() for prediction in revision_instance["GPT+FinetuningPred"]]
        self.filtered_fillers = filtered_fillers[key]["filtered_fillers"]
        self.revised_after_insertion = revision_instance["revised_after_insertion"]

    @property 
    def revised_untill_insertion(self): 
        if "revised_untill_insertion" in self.keys: 
           return self.revision_instance["revised_untill_insertion"]
        else: 
           return self.revision_instance["revised_until_insertion"]




def main(): 
    for key, _ in data.items(): 
        revision_object = RevisionInstance(key, data[key], data[key].keys())
        filler_in_sent = []
        for filler in revision_object.filtered_fillers:
            line = revision_object.revised_untill_insertion + " " + filler + " " + revision_object.revised_after_insertion
            filler_in_sent.append(line)
        
        print(filler_in_sent)
        break 


main()