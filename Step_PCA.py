import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

source = pd.read_csv('C:\Users\NYU\seaflow.csv')
newsource = source - source.mean()
datacov = newsource.cov()
eig_val_cov, eig_vec_cov = np.linalg.eig(datacov)
eig_pairs = [(np.abs(eig_val_cov[i]), eig_vec_cov[:,i]) for i in range(len(eig_val_cov))]
eig_pairs.sort()
eig_pairs.reverse()
matrix_w = np.hstack((eig_pairs[0][1].reshape(3,1), eig_pairs[1][1].reshape(3,1)))
transformed = newsource.as_matrix().dot(matrix_w)
plt.plot(transformed[0:19340,0],transformed[0:19340,1],\
     'o', markersize=7, color='blue', alpha=0.5, label='class1')


plt.show()