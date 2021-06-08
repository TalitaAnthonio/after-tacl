import json 
from load_embeddings import * 
import numpy as np 
from scipy import spatial
from sent2vec.vectorizer import Vectorizer
import pdb 

PATH_TO_FILE = "../coreference/filtered_predictions_step2.json"

with open(PATH_TO_FILE, "r") as json_in: 
     data = json.load(json_in)

print("load embeddings ..... ")
with open("glove.6B.50d.txt", "r") as embedding_file: 
     content = embedding_file.readlines()
     w2v = {}
     for line in content: 
         line = line.strip('\n').split()
         word = line[0]
         representation = np.array(list(map(float, line[1:])))
         w2v[word] = representation



def compute_distance(vec1, vec2): 
    return spatial.distance.cosine(vec1, vec2)


def vectorize_text(text_to_vectorize): 

    vectorizer = Vectorizer()
    vectorizer.bert(text_to_vectorize)
    vectors_bert = vectorizer.vectors

    return vectors_bert 



def get_repr_for_filtered(filtered_pred, before_insertion, after_insertion): 
    fillers_with_embedding = []

    vectorizer = MeanEmbeddingVectorizer(w2v, 50)
    for filler in filtered_pred: 
        original_with_filler = before_insertion + " " + filler + " " + after_insertion
        avg_repr = vectorizer.transform(original_with_filler)
        fillers_with_embedding.append([original_with_filler, float(avg_repr)])
    return fillers_with_embedding




def main(): 
    counter = 0 
    d = {}
    for key, _ in data.items(): 

        counter +=1 
        print("processing {0}".format(counter))
        print("======================================")
        revised_sentence = data[key]["revised_sentence"]
        rev_bert_repr = vectorize_text([revised_sentence])

        sents_with_distance_to_rev = []
        for filler in data[key]["filtered2"]: 
            if filler != data[key]["CorrectReference"]: 
                sent_with_filler = data[key]["revised_untill_insertion"] + " " + filler + " " + data[key]["revised_after_insertion"]
                pred_bert_repr = vectorize_text([sent_with_filler])

                distance_to_revised = compute_distance(rev_bert_repr, pred_bert_repr)
                sents_with_distance_to_rev.append([filler, sent_with_filler, distance_to_revised]) 

        sents_with_distance_to_rev_sorted = sorted(sents_with_distance_to_rev, key=lambda x: x[-1], reverse=False)
        
        d[key] = sents_with_distance_to_rev_sorted

        for elem in sents_with_distance_to_rev_sorted: 
            print(elem)



            print("============================================")
        

    with open("bert_embeddings_dict.json", "w") as json_out: 
         json.dump(d, json_out)

main()