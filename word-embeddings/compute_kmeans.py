
from scipy import spatial
from sent2vec.vectorizer import Vectorizer
from sklearn import cluster
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min
import json 
import pdb 
import numpy as np 
import pickle 


# TODO: 
# If the revised sentence is not among the top N (check of de index in the range is van (0,top_n))
# Als dat niet zo is: 
# Pak de top_n - 1 
# voeg de revised sentence toe (check de index en pak vanuit daar de sentence zoals ie in embeddings[sentences] staat en de vectorized represnetation )
# sentence_embeddings + revised-sentence 
# vectors + vector_of_revised_sentence 
# Maak dan de clusters 

PATH_TO_FILE = "../coreference/filtered_predictions_step2.json"
PATH_TO_EMBEDDINGS = "bert_vectors_POSTAG_new.pickle"
NUM_OF_PRED = 20
PATH_TO_FILE_OUT = "kmeans_k=5_filtered_step1_top{0}.json".format(NUM_OF_PRED)


with open(PATH_TO_EMBEDDINGS, "rb") as pickle_in: 
     embeddings = pickle.load(pickle_in) 



with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)


def vectorize_data(sentences): 
    vectorizer = Vectorizer()
    vectorizer.bert(sentences)
    vectors_bert = vectorizer.vectors

    return vectors_bert 



def get_clusters(vectorized_sentences, num_clusters=5):
    """
        Param: 
        --------------

        vectorized_sentences {list} with sentence representation: 
        the sentence in embedding representation. 
    """ 
    
    clustered_sentences = []
    km = KMeans(n_clusters=num_clusters)
    km.fit(vectorized_sentences)
    clusters = km.labels_.tolist()
    cluster_centers = km.cluster_centers_
    closest_data_indexes, _ = pairwise_distances_argmin_min(km.cluster_centers_, vectorized_sentences)
    return clusters, cluster_centers, closest_data_indexes
        


def main(): 

    d = {}
    for key, _ in data.items(): 
        print("------------------- {0} ------------------------------".format(key))
        revised_sentence = data[key]["revised_sentence"]


        if data[key]["CorrectReference"].lower() in [elem.lower() for elem in data[key]["filtered1"]][0:NUM_OF_PRED]:
            filtered_predictions = data[key]["filtered1"][0:NUM_OF_PRED]
            vectorized_sentences = embeddings[key]["vectors"][0:NUM_OF_PRED]
            sentences = embeddings[key]["sentences"][0:NUM_OF_PRED]


        else: 
            filtered_predictions = data[key]["filtered1"][0:NUM_OF_PRED-1]
            vectorized_sentences = embeddings[key]["vectors"][0:NUM_OF_PRED-1]
            sentences = embeddings[key]["sentences"][0:NUM_OF_PRED-1]

            # take the index of the filler
            pdb.set_trace() 
            index_of_revised = embeddings[key]["sentences"].index(revised_sentence)


        # add the revised sentence to the top predictions 
        sentences = sentences + [revised_sentence]

        # add the revised sentence to the top predictions 


        if len(filtered_predictions) > 4: 

            clusters, cluster_centers, closest_data_indexes = get_clusters(vectorized_sentences, num_clusters=5)
        
        elif len(filtered_predictions) == 1: 

            clusters, cluster_centers, closest_data_indexes = get_clusters(vectorized_sentences, num_clusters=1)

            
        else: 
            
            clusters, cluster_centers, closest_data_indexes = get_clusters(vectorized_sentences, num_clusters=len(filtered_predictions)//2)
        


        cluster_dict = {}
        for i in range(len(clusters)): 
            if clusters[i] in cluster_dict.keys(): 
               cluster_dict[clusters[i]].append(sentences[i])
            
            else: 
                cluster_dict[clusters[i]] = []
                cluster_dict[clusters[i]].append(sentences[i])

        
        print("revised", revised_sentence)
        for cluster_id, _ in cluster_dict.items(): 
            print("======= cluster {0} ==========".format(cluster_id))
            for sent in cluster_dict[cluster_id]: 
                print(sent)


        closest_to_centroids =  [sentences[index] for index in closest_data_indexes]
        print(closest_to_centroids)

        d[key] = {"clusters": cluster_dict, "centroids": closest_to_centroids}


    #with open(PATH_TO_FILE_OUT, "w") as json_out: 
    #        json.dump(d,json_out)
 
main()