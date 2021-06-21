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

PATH_TO_FILE = "../coreference/filtered_dev_preds_final.json"

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
        revised_sentence = data[key]["RevisedSentence"]
        filtered_predictions = data[key]["filtered_fillers"]
        print(filtered_predictions)

        # get embeddings for the fillers 
        sentences_with_filler = []
        for index, filler in enumerate(filtered_predictions,0): 
            
            sentence_with_filler = data[key]["revised_untill_insertion"] + " " + filler + " " + data[key]["revised_after_insertion"]
            sentences_with_filler.append(sentence_with_filler)



        
        # if there are no filtered predictions, leave empty. 
        if filtered_predictions == []:
           sentences_with_filler = [] 
           vectorized = []
        else: 
        
            vectorized = vectorize_data(sentences_with_filler)
            revised_sentence_embedding = vectorize_data([revised_sentence])

        d[key] = {"vectors": vectorized, "sentences": sentences_with_filler, "revised_sentence_embedding": revised_sentence_embedding, "revised_sentence": revised_sentence}

        counter +=1 

    
    np.save("bert_vectors_FINAL.npy", d)

    with open("bert_vectors_FINAL.pickle", "wb") as pickle_out: 
         pickle.dump(d, pickle_out)
    

 
main()