# Step 3: Make clusters 


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
import pdb 


#PATH_TO_FILE = "../coreference/filtered_predictions_step2.json"
#PATH_TO_FILE = "../data-cleaning/filtered_set_train.json"

#PATH_TO_FILE = "../data-cleaning/filtered_set_train.json"


PATH_TO_FILE = "../coreference/filtered_dev_preds_final_nouns_only.json"
PATH_TO_EMBEDDINGS =  "filtered_dev_preds_final_nouns_only_embeddings.pickle"
NUM_OF_PRED = 20
NUM_CLUSTERS = 5 

PATH_TO_FILE = "../coreference/filtered_dev_preds_final_nouns_only.json"
PATH_TO_FILE_OUT = "k_means_dev_set_filtered_latest_new.json".format(NUM_OF_PRED)


with open("human_inserted_reference_not_pronoun.pickle", "rb") as pickle_in: 
     subset = pickle.load(pickle_in)

keys = subset


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
    km = KMeans(n_clusters=num_clusters, random_state=1, max_iter=600, n_init=20)
    km.fit(vectorized_sentences)
    clusters = km.labels_.tolist()
    cluster_centers = km.cluster_centers_
    # get the points that are the closest to the centroid.
    closest_data_indexes, _ = pairwise_distances_argmin_min(km.cluster_centers_, vectorized_sentences)
    return clusters, cluster_centers, closest_data_indexes



def get_clusters(sentences, vectorized_sentences, filtered_predictions, index_of_revised, num_clusters=5): 
    if len(vectorized_sentences) > 4: 

        clusters, cluster_centers, closest_data_indexes = use_k_means(vectorized_sentences, num_clusters=num_clusters)
    
    elif len(vectorized_sentences) == 1 or len(filtered_predictions) == 0: 

        clusters, cluster_centers, closest_data_indexes = use_k_means(vectorized_sentences, num_clusters=1)

        
    else: 
        print("in else")
        clusters, cluster_centers, closest_data_indexes = use_k_means(vectorized_sentences, num_clusters=len(vectorized_sentences))


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
        print(cluster, sents)
        if index_of_revised in [sent[1] for sent in sents]: 
           cluster_dict_indexes_only[cluster] = {"sents": [sent[1] for sent in sents], "revised-in-cluster": True, "index_of_revised": index_of_revised}
        else: 
           cluster_dict_indexes_only[cluster] = {"sents": [sent[1] for sent in sents], "revised-in-cluster": False, "index_of_revised": index_of_revised}


    # filtered_centroids = centroids with revised 
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


def get_index_of_revised(predictions, correct_reference): 

    index_for_revised = []
    for index, prediction in enumerate(predictions,0): 
        if prediction.lower() == correct_reference.lower(): 
           index_for_revised.append(index)
           break 
        
    return index_for_revised




def main(): 
    d = {}
    for key, _ in data.items():  
        if key in keys: 
            print("------------------- {0} ------------------------------".format(key))

            revised_sentence = data[key]["RevisedSentence"]

            if type(data[key]["CorrectReference"]) == list: 
                reference = " ".join(data[key]["CorrectReference"])
            else: 
                reference = data[key]["CorrectReference"]
            


            index_of_revised = get_index_of_revised(embeddings[key]["filtered_fillers2"], reference)
            


            if index_of_revised != []: 
                index_of_revised = index_of_revised[0]
                if index_of_revised in [i for i in range(0,NUM_OF_PRED)]:
                    print("index in range")
                    filtered_predictions = embeddings[key]["filtered_fillers2"][0:NUM_OF_PRED]
                    vectorized_sentences = embeddings[key]["vectors"][0:NUM_OF_PRED]
                    sentences = embeddings[key]["sentences"][0:NUM_OF_PRED]


            
                # otherwise, add the revised sentence to the predictions 
                else: 
                    print("index not in range")
                    filtered_predictions = embeddings[key]["filtered_fillers2"][0:NUM_OF_PRED-1]
                    vectorized_sentences = embeddings[key]["vectors"][0:NUM_OF_PRED-1]
                    sentences = embeddings[key]["sentences"][0:NUM_OF_PRED-1]

                    revised_sentence_vector = embeddings[key]["revised_sentence_embedding"]
                    revised_sentence_repr = embeddings[key]["revised_sentence"]

                    sentences = sentences + [revised_sentence_repr]
                    vectorized_sentences = np.append(vectorized_sentences, revised_sentence_vector, axis=0)
                    index_of_revised = 19 

            else: 
                print("prediction not in top")
                filtered_predictions = embeddings[key]["filtered_fillers2"][0:NUM_OF_PRED-1]

                # length = 19 and length = 19 
                vectorized_sentences = embeddings[key]["vectors"][0:NUM_OF_PRED-1]
                sentences = embeddings[key]["sentences"][0:NUM_OF_PRED-1]


                revised_sentence_vector = embeddings[key]["revised_sentence_embedding"]
                revised_sentence_repr = embeddings[key]["revised_sentence"]
                index_of_revised = 19 
                

            

                if vectorized_sentences == []: 
                    sentences  = [revised_sentence]
                    vectorized_sentences = revised_sentence_vector
                else: 
                    sentences = sentences + [revised_sentence_repr]
                    vectorized_sentences = np.append(vectorized_sentences, revised_sentence_vector, axis=0)


            

            try: 
                assert len(sentences) == len(vectorized_sentences)
                assert index_of_revised != []
            except AssertionError: 
                pdb.set_trace()

            print(len(vectorized_sentences))
            cluster_dict, cluster_centers, closest_data_indexes, centroids_by_prob, centroids_with_revised = get_clusters(sentences, vectorized_sentences, filtered_predictions, index_of_revised, NUM_CLUSTERS)



            
            print("revised", revised_sentence)
            for cluster_id, _ in cluster_dict.items(): 
                print("======= cluster {0} ==========".format(cluster_id))
                for sent in cluster_dict[cluster_id]: 
                    print(sent)


            closest_to_centroids =  [sentences[index] for index in closest_data_indexes]
            centroids_with_revised_sents = [sentences[index] for index in centroids_with_revised]

            print(len(filtered_predictions))
            print(len(sentences))

            if len(sentences) != len(filtered_predictions): 
               selected_centroids = [filtered_predictions[index] for index in centroids_with_revised if index in range(0,len(filtered_predictions))]
            else: 
                selected_centroids = [filtered_predictions[index] for index in centroids_with_revised]
           
            print(selected_centroids)
            d[key] = {"clusters": cluster_dict, "centroids": closest_to_centroids, "centroids_by_prob": centroids_by_prob, "Centroids_with_revised": centroids_with_revised_sents, "SelectedCentroids": selected_centroids}
            d[key].update(data[key])

            print("centroids with revised", centroids_with_revised_sents)
   

    with open(PATH_TO_FILE_OUT, "w") as json_out: 
                json.dump(d,json_out)


main()