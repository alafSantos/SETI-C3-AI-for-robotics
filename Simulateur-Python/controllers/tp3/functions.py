'''
Developed by Alaf DO NASCIMENTO SANTOS in the context of the Artificial Intelligence for Robotics course. Master SETI.

given functions file
'''

import numpy as np
from scipy.spatial import cKDTree as KDTree

'''
zoefjzoe

'''
def indxtMean(index,arrays):
    indxSum = np.array([0.0, 0.0 ,0.0])
    for i in range(np.size(index,0)):
        indxSum = np.add(indxSum, np.array(arrays[index[i]]), out = indxSum ,casting = 'unsafe')
    return indxSum/np.size(index,0)

'''
afineizagezok

'''
def indxtfixed(index,arrays):
    T = []
    for i in index:
        T.append(arrays[i])
    return np.asanyarray(T)

'''
Iterated Closest Points (ICP) function

La fonction ICP prend comme paramètres les coordonnées x,y des points fixes (les murs dans notre cas) et 
les coordonnées xy des points mobiles (télémètres laser) que l’on souhaite recaler avec sur les murs. Elle 
calcule la transformation (rotation + translation) pour replacer au mieux les données télémètres sur les murs.
'''
def ICPSVD(fixedX, fixedY, movingX, movingY):
    reqR = np.identity(3) # Return a identity matrix
    reqT = [0.0, 0.0, 0.0] # 
    fixedt = []
    movingt = []
    
    for i in range(len(fixedX)):
        fixedt.append([fixedX[i], fixedY[i], 0])
    
    for i in range(len(movingX)):
        movingt.append([movingX[i], movingY[i], 0])

    moving = np.asarray(movingt)
    fixed = np.asarray(fixedt)
    n = np.size(moving,0) # pas sur
    TREE = KDTree(fixed)
    
    for i in range(10):
        distance, index = TREE.query(moving)
        err = np.mean(distance**2)

        com = np.mean(moving,0)
        cof = indxtMean(index,fixed)
        W = np.dot(np.transpose(moving),indxtfixed(index,fixed)) - n*np.outer(com,cof) 
        U , _ , V = np.linalg.svd(W, full_matrices = False)

        tempR = np.dot(V.T,U.T)
        tempT = cof - np.dot(tempR,com)
        
        moving = (tempR.dot(moving.T)).T
        moving = np.add(moving,tempT) 
        reqR=np.dot(tempR,reqR)
        reqT = np.add(np.dot(tempR,reqT),tempT)

