import numpy as np
from sklearn.datasets import make_blobs

# Set the random seed for reproducibility
np.random.seed(0)

# Generate the data
n_samples = 300
n_clusters = 5
X, y = make_blobs(n_samples=n_samples, centers=n_clusters, random_state=1)

# Scale the data to range between 0 and 100
X = (X - np.min(X)) / (np.max(X) - np.min(X)) * 100

# Save the data to the file
file_path = r'C:\Users\Dell\source\repos\232ccdd3-gr21-repo\FInalny_Projekt\dataset.txt'
np.savetxt(file_path, X, fmt='%.8f', delimiter=' ')
