import numpy as np
from sklearn.datasets import make_blobs
import time
from datetime import datetime
np.random.seed(int(time.time()))



# generuj
n_samples = 100
n_clusters = 5
X, y = make_blobs(n_samples=n_samples, centers=n_clusters, random_state=1)

#0-100
X = (X - np.min(X)) / (np.max(X) - np.min(X)) * 100

# zapisz
file_path = r'C:\Users\Dell\source\repos\232ccdd3-gr21-repo\FInalny_Projekt\dataset.txt'
np.savetxt(file_path, X, fmt='%.8f', delimiter=' ')
