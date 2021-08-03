import pickle 

#Steam_Vegetables67

with open("bert_vectors_FINAL_dev_top100_nouns_only.pickle", "rb") as json_in: 
     embeddings = pickle.load(json_in)


print(embeddings["Steam_Vegetables67"]["sentences"])
print(embeddings["Steam_Vegetables67"]["filtered_fillers"])

