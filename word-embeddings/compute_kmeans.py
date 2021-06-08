
from scipy import spatial
from sent2vec.vectorizer import Vectorizer
from sklearn import cluster
from sklearn.cluster import KMeans
import json 
import pdb 


PATH_TO_FILE = "../coreference/filtered_predictions_step2.json"

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)

#sentences = [
#  "Cook the steak to medium rare.", "Cook the chicken to medium rare", "Cook your dish to medium rare"
#]

#vectorizer = Vectorizer()
#vectorizer.bert(sentences)
#vectors_bert = vectorizer.vectors
#print(vectors_bert)

#km = KMeans(n_clusters=2)
#km.fit(vectors_bert)
#clusters = km.labels_.tolist()
#print(clusters)

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
    return clusters 
        


def main(): 

    for key, _ in data.items(): 
        print("------------------- {0} ------------------------------".format(key))
        revised_sentence = data[key]["revised_sentence"]
        filtered_predictions = data[key]["filtered2"]

        # get the top fillers 
        sentences_with_filler = []
        for filler in filtered_predictions: 
            if filler.lower() != data[key]["CorrectReference"].lower(): 
                sentence_with_filler = data[key]["revised_untill_insertion"] + " " + filler + " " + data[key]["revised_after_insertion"]
                sentences_with_filler.append(sentence_with_filler)
        
        sentences_with_filler.append(revised_sentence)
        
        # vectorize 
        vectorized = vectorize_data(sentences_with_filler)

        # get clusters 

        print(len(sentences_with_filler))
        if len(sentences_with_filler) > 4: 
            clusters = get_clusters(vectorized, n_clusters=5)
        elif len(sentences_with_filler) == 1: 
            clusters = get_clusters(vectorized, n_clusters=1)
        else: 
            clusters = get_clusters(vectorized, n_clusters=len(sentences_with_filler)//2 )
        
        # check to which cluster each sentence belongs 

        cluster_dict = {}
        for sentence, cluster in zip(sentences_with_filler, clusters): 
            if cluster in cluster_dict.keys(): 
               cluster_dict[cluster].append(sentence)
            else: 
                cluster_dict[cluster] = []
                cluster_dict[cluster].append(sentence)
        
        print(cluster_dict)
        for clusternr, sentences in cluster_dict.items(): 
            print("==== cluster {0} ====".format(clusternr)) 
            for sentence in cluster_dict[clusternr]: 
                print(sentence)
        


     


main()