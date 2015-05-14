#Author/Developer: Elton Dias
#Date: 5/6/2015
#Description: Pipeline -> PCA - Silhouette Score Computation for K Value - Plots KMeans based on Value of K

import glob
import os.path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pprint
import collections
import operator
import csv
import warnings
import matplotlib.pylab
from collections import Counter
warnings.filterwarnings("ignore", 'Mean of empty slice.')
from sklearn.cluster import KMeans
from sklearn import metrics
from pylab import *

def CreateList(Locale):
    ListOfFiles = []
    for name in glob.glob(Locale):
        ListOfFiles.append(name)
    return ListOfFiles

def Create_Principal_Components(f):
    MatrixDict = {}
    MatrixDict['Eigenvalue0'] = []
    MatrixDict['Eigenvector01'] = []
    MatrixDict['Eigenvector02'] = [] 
    MatrixDict['Eigenvector03'] = []     
    MatrixDict['Eigenvalue1'] = []
    MatrixDict['Eigenvector11'] = []
    MatrixDict['Eigenvector12'] = [] 
    MatrixDict['Eigenvector13'] = []         
    source = pd.read_csv(f, usecols=['fsc_adj','chl_adj','pe_adj'])    
    newsource = source - source.mean()    
    evals, evecs = np.linalg.eig((newsource.cov()).T)
    order = evals.argsort()[::-1]
    NewList = [evals[order[0]]] + [i for i in evecs[:,order[0]]] + [evals[order[1]]] + [i for i in evecs[:,order[1]]]
    MatrixDict['Eigenvalue0'].append(NewList[0])
    MatrixDict['Eigenvector01'].append(NewList[1])
    MatrixDict['Eigenvector02'].append(NewList[2])
    MatrixDict['Eigenvector03'].append(NewList[3])
    MatrixDict['Eigenvalue1'].append(NewList[4])
    MatrixDict['Eigenvector11'].append(NewList[5])
    MatrixDict['Eigenvector12'].append(NewList[6])
    MatrixDict['Eigenvector13'].append(NewList[7])
    print "PCA Completed for " + f
    return MatrixDict    

def Compute_Silhouette_Score(f):
    NoOfClusters = collections.defaultdict()
    Get_PCA_Data = np.genfromtxt(f, delimiter=",", skiprows=1)
    PCA_Data = Get_PCA_Data[:,[2,3,4]]
    for i in range(2,8):
        kmeans_model = KMeans(n_clusters=i, random_state=1).fit(PCA_Data)
        labels = kmeans_model.labels_  
        NoOfClusters[i] = metrics.silhouette_score(PCA_Data, labels, metric='euclidean')
    return max(NoOfClusters.iteritems(), key=operator.itemgetter(1))[0]

def Compute_KMeans(f,K):
    FigFile = "C:\Users\NYU\EigenComponents" + ".png"
    Get_PCA_Data = np.genfromtxt(f, delimiter=",", skiprows=1)
    PCA_Data = Get_PCA_Data[:,[2,3,4,6,7,8]]
    kmeans = KMeans(n_clusters=K)
    kmeans.fit(PCA_Data)
    #Plotting Figure Starts 
    fig = plt.figure(figsize=(20,10))    
    
    figure_title = "Component 1"
    
    plt.subplot(2,3,1)
    plt.scatter(PCA_Data[:,0],PCA_Data[:,1], s=15, c=kmeans.labels_, edgecolor='none')
    plt.xlabel("EVal 0 - EigenVector 1")
    plt.ylabel("EVal 0 - EigenVector 2")  

    ax = plt.subplot(2,3,2)
    plt.subplot(2,3,2)
    plt.scatter(PCA_Data[:,1],PCA_Data[:,2], s=15, c=kmeans.labels_, edgecolor='none')
    plt.xlabel("EVal 0 - EigenVector 2")
    plt.ylabel("EVal 0 - EigenVector 3")     
        
    plt.subplot(2,3,3)
    plt.scatter(PCA_Data[:,0],PCA_Data[:,2], s=15, c=kmeans.labels_, edgecolor='none')
    plt.xlabel("EVal 0 - EigenVector 1")
    plt.ylabel("EVal 0 - EigenVector 3") 
   
    
    plt.text(0.5, 1.08, figure_title,
         horizontalalignment='center',
         fontsize=20,
         transform = ax.transAxes
         )

    figure_title = "Component 2"

    plt.subplot(2,3,4)
    plt.scatter(PCA_Data[:,3],PCA_Data[:,4], s=15, c=kmeans.labels_, edgecolor='none')
    plt.xlabel("EVal 1- EigenVector 1")
    plt.ylabel("EVal 1 - EigenVector 2")  

    ax = plt.subplot(2,3,5)
    plt.subplot(2,3,5)
    plt.scatter(PCA_Data[:,4],PCA_Data[:,5], s=15, c=kmeans.labels_, edgecolor='none')
    plt.xlabel("EVal 1 - EigenVector 2")
    plt.ylabel("EVal 1 - EigenVector 3")  

    plt.subplot(2,3,6)
    plt.scatter(PCA_Data[:,3],PCA_Data[:,5], s=15, c=kmeans.labels_, edgecolor='none')
    plt.xlabel("EVal 1 - EigenVector 1")
    plt.ylabel("EVal 1 - EigenVector 3")  

    plt.text(0.5, 1.08, figure_title,
         horizontalalignment='center',
         fontsize=20,
         transform = ax.transAxes
         )           
       
    subplots_adjust(left=0.125, bottom=0.1, right=0.9, top=0.9, wspace=0.2, hspace=0.5)
    plt.savefig(FigFile)
    plt.clf()

def main():
    ListofList = []
    Dict_KMeans = {}
    path = "C:\Users\NYU\Cap\*"
    OPFile = 'C:\Users\NYU\Capstone.csv'
    FileList = CreateList(path)
    for i in FileList:
        Dict_KMeans = Counter(Dict_KMeans) + Counter(Create_Principal_Components(i))
    FinalMatrix = pd.DataFrame(Dict_KMeans, columns=['Eigenvalue0','Eigenvector01','Eigenvector02','Eigenvector03','Eigenvalue1','Eigenvector11','Eigenvector12','Eigenvector13'])
    FinalMatrix.to_csv(OPFile)
    Compute_KMeans(OPFile,Compute_Silhouette_Score(OPFile))
    
    
if __name__ == "__main__":
    main()