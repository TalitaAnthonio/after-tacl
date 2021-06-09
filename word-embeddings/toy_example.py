from sklearn.cluster import KMeans 
import numpy as np
from sklearn.metrics import pairwise_distances_argmin_min
import pdb 

X = np.array([[1.0 , 2.0], [1.0, 4.0], [1.0, 0.0], [10.0, 2.1], [10.1, 4.1], [10.2, 0.2]])
kmeans = KMeans(n_clusters=2, random_state=0).fit(X)
print(kmeans.labels_) 
print("clusters")
print(kmeans.cluster_centers_) 

print("data")
print(X)


closest, _ = pairwise_distances_argmin_min(kmeans.cluster_centers_, X) 
print(closest)
pdb.set_trace()