import glob
import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def CreateList(Locale):
    ListOfFiles = []
    for name in glob.glob(Locale):
        ListOfFiles.append(name)
    return ListOfFiles

def Run_PCA(f):
    FigFile = f[:-3]+"png"
    if FigFile.find("Tok") == -1:
        col = "blue"
    else:
        col = "red"
    source = pd.read_csv(f)
    newsource = source - source.mean()
    datacov = newsource.cov()
    eig_val_cov, eig_vec_cov = np.linalg.eig(datacov)
    eig_pairs = [(np.abs(eig_val_cov[i]), eig_vec_cov[:,i]) for i in range(len(eig_val_cov))]
    eig_pairs.sort()
    eig_pairs.reverse()
    matrix_w = np.hstack((eig_pairs[0][1].reshape(3,1), eig_pairs[1][1].reshape(3,1)))
    transformed = newsource.as_matrix().dot(matrix_w)
    plt.plot(transformed[0:len(source),0],transformed[0:len(source),1],\
         'o', markersize=7, color=col, alpha=0.5, label='class1')  
    plt.savefig(FigFile)
    plt.clf()


def main():
    Images = []
    path = "C:\Users\NYU\SeaFlow2\*"
    FileList = CreateList(path)
    for i in FileList:
        Images = Run_PCA(i)       


if __name__ == "__main__":
    main()




    
