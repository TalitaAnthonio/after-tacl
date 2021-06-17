
from operator import index
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
NUM_CLUSTERS = 5 
PATH_TO_FILE_OUT = "kmeans_k=5_filtered_step1_top{0}_with_rev.json".format(NUM_OF_PRED)


with open(PATH_TO_EMBEDDINGS, "rb") as pickle_in: 
     embeddings = pickle.load(pickle_in) 



with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)


def vectorize_data(sentences): 
    vectorizer = Vectorizer()
    vectorizer.bert(sentences)
    vectors_bert = vectorizer.vectors

    return vectors_bert 



def use_k_means(vectorized_sentences, num_clusters=5):
    """
        Param: 
        --------------

        vectorized_sentences {list} with sentence representation: 
        the sentence in embedding representation. 

        num_cluster {int}: the number of clusters to use, default = 5
    """ 
    
    clustered_sentences = []
    km = KMeans(n_clusters=num_clusters)
    km.fit(vectorized_sentences)
    clusters = km.labels_.tolist()
    cluster_centers = km.cluster_centers_
    # get the points that are the closest to the centroid.
    closest_data_indexes, _ = pairwise_distances_argmin_min(km.cluster_centers_, vectorized_sentences)
    return clusters, cluster_centers, closest_data_indexes



def get_clusters(sentences, vectorized_sentences, filtered_predictions, index_of_revised, num_clusters=5): 
    if len(filtered_predictions) > 4: 

        clusters, cluster_centers, closest_data_indexes = use_k_means(vectorized_sentences, num_clusters=num_clusters)
    
    elif len(filtered_predictions) == 1: 

        clusters, cluster_centers, closest_data_indexes = use_k_means(vectorized_sentences, num_clusters=1)

        
    else: 
        
        clusters, cluster_centers, closest_data_indexes = use_k_means(vectorized_sentences, num_clusters=len(filtered_predictions)//2)


    # make a dictionary with the clusters {"1": sent1, sent2, sent3, "2": sent4, sent5, sent6}
    cluster_dict = {}
    for i in range(len(clusters)): 
        if clusters[i] in cluster_dict.keys(): 
            cluster_dict[clusters[i]].append([sentences[i], i])   
        else: 
            cluster_dict[clusters[i]] = []
            cluster_dict[clusters[i]].append([sentences[i], i])


    # do not use the centroids but the sentence with the highest probability as provided by the GPT model. 
    centroids_by_prob = []
    for cluster, sents in cluster_dict.items():     
        biggest_prob = sorted(cluster_dict[cluster], key=lambda x: x[-1])[0][0]
        centroids_by_prob.append(biggest_prob)
    

    # make a dict with just the clusters and the indexes to check later which of them has the revised sentence. 
    cluster_dict_indexes_only = {}
    for cluster, sents in cluster_dict.items(): 
        if index_of_revised in [sent[1] for sent in sents]: 
           cluster_dict_indexes_only[cluster] = {"sents": [sent[1] for sent in sents], "revised-in-cluster": True, "index_of_revised": index_of_revised}
        else: 
           cluster_dict_indexes_only[cluster] = {"sents": [sent[1] for sent in sents], "revised-in-cluster": False, "index_of_revised": index_of_revised}



    filtered_centroids = []
    for index in closest_data_indexes: 
        for key, _ in cluster_dict_indexes_only.items(): 
            if index in cluster_dict_indexes_only[key]["sents"]: 
                if cluster_dict_indexes_only[key]["revised-in-cluster"] == False: 
                   #filtered_centroids.append([key, index])
                   filtered_centroids.append(index)
                else: 
                    #filtered_centroids.append([key, cluster_dict_indexes_only[key]["index_of_revised"]])
                    filtered_centroids.append(cluster_dict_indexes_only[key]["index_of_revised"])


    return cluster_dict, cluster_centers, closest_data_indexes, centroids_by_prob, filtered_centroids


def main(): 

    d = {}
    for key, _ in data.items(): 
        print("------------------- {0} ------------------------------".format(key))
        revised_sentence = data[key]["revised_sentence"]
        index_of_revised = embeddings[key]["index_of_revised_sentence"]
        print("index of revised", index_of_revised)
        
        # if the revised sentence is in there: 
        if index_of_revised in [i for i in range(0,NUM_OF_PRED)]:
            print("index in range")
            filtered_predictions = data[key]["filtered1"][0:NUM_OF_PRED]
            vectorized_sentences = embeddings[key]["vectors"][0:NUM_OF_PRED]
            sentences = embeddings[key]["sentences"][0:NUM_OF_PRED]


      
        # otherwise, add the revised sentence to the predictions 
        else: 
            print("index not in range")
            filtered_predictions = data[key]["filtered1"][0:NUM_OF_PRED-1]
            vectorized_sentences = embeddings[key]["vectors"][0:NUM_OF_PRED-1]
            sentences = embeddings[key]["sentences"][0:NUM_OF_PRED-1]

            revised_sentence_vector = embeddings[key]["vectors"][index_of_revised]
            revised_sentence_repr = embeddings[key]["sentences"][index_of_revised]

            index_of_revised = len(filtered_predictions)-1

            sentences = sentences + [revised_sentence_repr]
            vectorized_sentences = vectorized_sentences + revised_sentence_vector

            if key == "Claim_Your_Listing_With_Google0": 
                pdb.set_trace()


        print(len(filtered_predictions))

        cluster_dict, cluster_centers, closest_data_indexes, centroids_by_prob, centroids_with_revised = get_clusters(sentences, vectorized_sentences, filtered_predictions, index_of_revised, NUM_CLUSTERS)


 
        
        print("revised", revised_sentence)
        for cluster_id, _ in cluster_dict.items(): 
            print("======= cluster {0} ==========".format(cluster_id))
            for sent in cluster_dict[cluster_id]: 
                print(sent)


        closest_to_centroids =  [sentences[index] for index in closest_data_indexes]
        centroids_with_revised_sents = [sentences[index] for index in centroids_with_revised]

        d[key] = {"clusters": cluster_dict, "centroids": closest_to_centroids, "centroids_by_prob": centroids_by_prob, "Centroids_with_revised": centroids_with_revised_sents}


        print(centroids_by_prob)

        with open(PATH_TO_FILE_OUT, "w") as json_out: 
                json.dump(d,json_out)
 

main()