# Step 2: Make Bert Embeddings. 

from scipy import spatial
from sent2vec.vectorizer import Vectorizer
from sklearn import cluster
from sklearn.cluster import KMeans
import json 
import pdb 
import numpy as np 
import pickle
from sklearn.metrics import pairwise_distances_argmin_min

#PATH_TO_FILE = "../coreference/filtered_train_preds_final.json" 
PATH_TO_FILE = "../coreference/filtered_dev_preds_final_nouns_only.json"

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)

def vectorize_data(sentences): 
    vectorizer = Vectorizer()
    vectorizer.bert(sentences)
    vectors_bert = vectorizer.vectors

    return vectors_bert 

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




def main(): 

    d = {}
    counter = 0 
    for key, _ in data.items(): 
        counter +=1 
        print("------------------- {0} ------------------------------".format(counter))
        revised_sentence = data[key]["RevisedSentence"]
        filtered_predictions = data[key]["filtered_fillers"]


        if data[key]['reference-type'] == "bigram": 
            predictions_new = filter_second_step(data[key]["filtered_fillers"])
            filtered_predictions = [predictions_new[key][0] for key, _ in predictions_new.items()]


        # get embeddings for the fillers 
        sentences_with_filler = []
        for index, filler in enumerate(filtered_predictions,0): 
            if "revised_after_insertion" in data[key].keys(): 
                sentence_with_filler = data[key]["revised_untill_insertion"] + " " + filler + " " + data[key]["revised_after_insertion"]
                sentences_with_filler.append(sentence_with_filler)
            else: 
                sentence_with_filler = data[key]["revised_untill_insertion"] + " " + filler + " " + data[key]["revised_afer_insertion"]
                sentences_with_filler.append(sentence_with_filler)



        
        # if there are no filtered predictions, leave empty. 
        if filtered_predictions == []:
           sentences_with_filler = [] 
           vectorized = []
           revised_sentence_embedding = vectorize_data([revised_sentence])
        else: 
            vectorized = vectorize_data(sentences_with_filler)
            revised_sentence_embedding = vectorize_data([revised_sentence])

        d[key] = {"vectors": vectorized, "sentences": sentences_with_filler, "revised_sentence_embedding": revised_sentence_embedding, "revised_sentence": revised_sentence, 
        "filtered_fillers": filtered_predictions}

        

    
    np.save("bert_vectors_FINAL_dev_top100_nouns_only.npy", d)

    with open("bert_vectors_FINAL_dev_top100_nouns_only.pickle", "wb") as pickle_out: 
         pickle.dump(d, pickle_out)
    

 
main()