
from scipy import spatial
from sent2vec.vectorizer import Vectorizer
from sklearn import cluster
from sklearn.cluster import KMeans
import json 
import pdb 
import numpy as np 
import pickle
from sklearn.metrics import pairwise_distances_argmin_min

PATH_TO_FILE = "../coreference/filtered_predictions_step2.json"

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)

def vectorize_data(sentences): 
    vectorizer = Vectorizer()
    vectorizer.bert(sentences)
    vectors_bert = vectorizer.vectors

    return vectors_bert 



def get_clusters(vectorized_sentences, n_clusters=5):
    """
        Param: 
        --------------

        vectorized_sentences {list} with sentence representation: 
        the sentence in embedding representation. 
    """ 
    
    clustered_sentences = []
    km = KMeans(n_clusters=n_clusters)
    km.fit(vectorized_sentences)
    clusters = km.labels_.tolist()
    cluster_centers = km.cluster_centers_
    return clusters, cluster_centers 
        


def main(): 

    d = {}
    counter = 0 
    for key, _ in data.items(): 
        print("------------------- {0} ------------------------------".format(key))
        revised_sentence = data[key]["revised_sentence"]
        filtered_predictions = data[key]["filtered1"]

        # get embeddings for the fillers 
        sentences_with_filler = []
        for filler in filtered_predictions: 
            
            sentence_with_filler = data[key]["revised_untill_insertion"] + " " + filler + " " + data[key]["revised_after_insertion"]
            sentences_with_filler.append(sentence_with_filler)

        
        
        # if the reference is not among the filtered predictions, then add it to the list. 
        if data[key]["CorrectReference"].lower() not in filtered_predictions: 
           sentences_with_filler.append(revised_sentence)

        
        # vectorize 
        vectorized = vectorize_data(sentences_with_filler)
        d[key] = {"vectors": vectorized, "sentences": sentences_with_filler}

        counter +=1 

    
    np.save("bert_vectors_POSTAG_new.npy", d)


    with open("bert_vectors_POSTAG_new.pickle", "wb") as pickle_out: 
         pickle.dump(d, pickle_out)
 
main()