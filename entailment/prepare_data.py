# used to prepare data to test the model. 
import json 
import pdb 
import pandas as pd 

# dict_keys(['GPT+Finetuning+P-perplexityPred', 'GPT+Finetuning+P-perplexityCorr', 'GPT+FinetuningCorrect', 'CorrectReference', 'LeftContext', 'GPTPred', 'GPTCorrect', 'key', 'GPT+FinetuningPred', 'RevisedSentence', 'revised_untill_insertion', 'revised_after_insertion', 'reference-type', 'par', 'language_model_text', 'index_of_reference'])

path_to_pred_dir = "/Users/talita/Documents/PhD/tacl/analyse-predictions" 
path_to_file_with_predictions = '{0}/bestmodels_predictions.json'.format(path_to_pred_dir)
path_to_filtered_fillers = "../coreference/dev_set_with_filtered_fillers.json"


with open(path_to_file_with_predictions, "r") as json_in: 
     data = json.load(json_in)

# read the files here 

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


def make_df(data): 
    df = pd.DataFrame.from_dict(data)
    return df 


def main():
    d = {"x": [], "y": [], "context_x": [], "context_y": []} 
    for key, _ in data.items():

        revision_object = RevisionInstance(key, data[key], data[key].keys())
        print(revision_object.filtered_fillers)
        first_filler = revision_object.filtered_fillers[0]

        if len(revision_object.filtered_fillers) > 1: 
           second_filler = revision_object.filtered_fillers[1]
           if second_filler == first_filler: 
              second_filler = revision_object.filtered_fillers[2]
        else: 
           second_filler = revision_object.predictions[1]
           if second_filler == first_filler: 
              second_filler = revision_object.filtered_fillers[2]
        
      

        print(first_filler)
        print(second_filler)

        d["x"].append(first_filler)
        d["y"].append(second_filler)

        context_x = revision_object.revised_untill_insertion + " " + "<x>" + first_filler +  "</x>" + " " + revision_object.revised_after_insertion
        context_y = revision_object.revised_untill_insertion + " " + "<y>" + second_filler + "</y>" + " " + revision_object.revised_after_insertion

        d["context_x"].append(context_x)
        d["context_y"].append(context_y)

    df = make_df(d)
    df.to_csv("dev_set_wikihow.csv", index=False)

main()

