'''
Developed by Alaf DO NASCIMENTO SANTOS in the context of the Artificial Intelligence for Robotics course. Master SETI.

given functions file
'''

import math
import numpy as np
from scipy.spatial import cKDTree as KDTree

def multmatr(X,Y,T):
    res = []
    res.append( X[0] * Y[0] + X[3] * Y[1] + X[6] * Y[2] - T[0])
    res.append( X[1] * Y[0] + X[4] * Y[1] + X[7] * Y[2] + T[1])
    res.append( X[2] * Y[0] + X[5] * Y[1] + X[8] * Y[2] + T[2])
    return res

# This function is called when we are in the keyboard mode
def keyboard_control(keyboard, Keyboard, motor_left, motor_right, speed):
    key=keyboard.getKey()
    
    if (key==Keyboard.UP):
        motor_left.setVelocity(speed)
        motor_right.setVelocity(speed)
        
    elif (key==Keyboard.DOWN):
        motor_left.setVelocity(-speed)
        motor_right.setVelocity(-speed)
    
    elif(key==Keyboard.LEFT):
        motor_left.setVelocity(-speed)
        motor_right.setVelocity(speed)
    
    elif(key==Keyboard.RIGHT):
        motor_left.setVelocity(speed)
        motor_right.setVelocity(-speed)

    else:
        motor_left.setVelocity(0)
        motor_right.setVelocity(0)


def lidar_control(lidar, node, pose):
    point_cloud = lidar.getRangeImage() # a 360-size list
    angle = 0
    rotation = node.getOrientation()
    xyz_ref = node.getPosition()
    xyz = [pose['x'], 0, pose['y']]
    x_list = []
    y_list = []
    x_list_ref = []
    y_list_ref = []

    for i in point_cloud:
        xy = [i*math.sin(angle), 0, i*math.cos(angle)]
        
        pt = multmatr(rotation,xy,xyz)
        x_list.append(100*pt[0])
        y_list.append(100*pt[2])
        
        pt_ref = multmatr(rotation,xy,xyz_ref)
        x_list_ref.append(100*pt_ref[0])
        y_list_ref.append(100*pt_ref[2])

        angle += 2*math.pi / lidar.getHorizontalResolution()

    return x_list, y_list, x_list_ref, y_list_ref, xyz_ref

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

