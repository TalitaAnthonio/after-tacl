import json 
from load_embeddings import * 
import numpy as np 
import pdb 

with open("glove.6B.50d.txt", "r") as word2vecfile:
    content = word2vecfile.readlines()
    w2v = {}
    for line in content: 
        line = line.strip('\n').split()
        word = line[0]
        representation = np.array(list(map(float, line[1:])))
        w2v[word] = representation 
    


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
        self.predictions = [prediction.strip() for prediction in revision_instance["GPT+Finetuning+P-perplexityPred"]]
        self.filtered_fillers = filtered_fillers[key]["filtered_fillers"]
        self.revised_after_insertion = revision_instance["revised_after_insertion"]
        self.reference_type = revision_instance["reference-type"]

    @property 
    def revised_untill_insertion(self): 
        if "revised_untill_insertion" in self.keys: 
           return self.revision_instance["revised_untill_insertion"]
        else: 
           return self.revision_instance["revised_until_insertion"]

    #@property 
    #def dict_with_fillers(self): 


def filter_second_step(filtered_fillers): 
    d = {}
    for elem in filtered_fillers: 

        if len(elem.split()) == 2: 
            noun = elem.split()[1]
        else: 
            noun = elem 
        if noun in d.keys(): 
            d[noun].append(elem) 
        else: 
            d[noun] = []
            d[noun].append(elem)

    return d 


def main(): 
    for key, _ in data.items(): 
        revision_object = RevisionInstance(key, data[key], data[key].keys())
        if revision_object.reference_type == "bigram": 
           print("========================")
           print(key)
           print("revised sentence", data[key]["RevisedSentence"])
           print("filtered", revision_object.filtered_fillers)
           
           print("========= similar words =====================")
           filtered = filter_second_step(revision_object.filtered_fillers)
           fillers_to_keep = [filtered[noun][0] for noun, _ in filtered.items() if noun not in ["the", "a"]]
           print(fillers_to_keep)

           #print("filtered", filtered)

        """        
        filler_repr = []

        print(revision_object.filtered_fillers)
        for filler in revision_object.filtered_fillers:
            noun = filler.split()[1]
            line = revision_object.revised_untill_insertion + " " + noun + " " + revision_object.revised_after_insertion
            vectorizer = MeanEmbeddingVectorizer(w2v, 50)
            embeddings = vectorizer.transform(line.lower().split())
            filler_repr.append([line, list(embeddings)[0], filler])
        
        sorted_filler_repr = sorted(filler_repr, key=lambda x:x[1], reverse=True)
        for elem in sorted_filler_repr: 
            print(elem)
        
        break 
        """ 

main()