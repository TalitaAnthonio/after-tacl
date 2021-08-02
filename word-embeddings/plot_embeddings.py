
# Plot the embeddings. 

import pickle 
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt



PATH_TO_EMBEDDINGS = "bert_vectors_FINAL_train_top100.pickle"
key = "Cook_a_Potato_in_the_Microwave13"


with open(PATH_TO_EMBEDDINGS, "rb") as pickle_in: 
     embeddings = pickle.load(pickle_in) 

labels = embeddings[key]['sentences']
tokens = embeddings[key]['vectors']


tsne_model = TSNE(perplexity=40, n_components=2, init='pca', n_iter=2500, random_state=23)
new_values = tsne_model.fit_transform(tokens)

x = []
y = []
for value in new_values:
    x.append(value[0])
    y.append(value[1])
    
plt.figure(figsize=(16, 16)) 
for i in range(len(x)):
    plt.scatter(x[i],y[i])
    plt.annotate(labels[i],
                    xy=(x[i], y[i]),
                    xytext=(5, 2),
                    textcoords='offset points',
                    ha='right',
                    va='bottom')
plt.show()
    