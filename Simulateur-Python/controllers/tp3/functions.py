'''
Developed by Alaf DO NASCIMENTO SANTOS in the context of the Artificial Intelligence for Robotics course. Master SETI.

Additional functions file
'''

import math
import numpy as np
from scipy.spatial import cKDTree as KDTree
from graph_walls import graphWalls

t_previous = 0 # Global variable used when doing ICP (get the previous timestamp)

'''
This function is called when we are in the keyboard mode
'''
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


'''
This function is called when using LIDAR measurements
'''
def lidar_control(lidar, node, pose, kinematics, t_current):
    global t_previous

    point_cloud = lidar.getRangeImage() # a 360-size list
    angle = 0
    rotation_ref = node.getOrientation()
    rotation = kinematics.rotation_matrix(pose["theta"])
    xyz_ref = node.getPosition()
    xyz = [pose['x'], 0, pose['y']]
    x_list = []
    y_list = []
    x_list_ref = []
    y_list_ref = []

    walls_x_list, walls_y_list = graphWalls.get_disc_walls()

    for point in point_cloud:
        xy = [point*math.sin(angle), 0, point*math.cos(angle)]
        
        pt = multmatr(rotation,xy,xyz)
        x_list.append(100*pt[0])
        y_list.append(100*pt[2])

        pt_ref = multmatr(rotation_ref,xy,xyz_ref)
        x_list_ref.append(100*pt_ref[0])
        y_list_ref.append(100*pt_ref[2])

        angle += 2*math.pi / lidar.getHorizontalResolution()

    if t_current - t_previous >= 5 : # calculate the transformation every 5 seconds
        t_previous = t_current
        accept_flag, reqR, reqT = ICPSVD(walls_x_list, walls_y_list, x_list, y_list)
        

        if accept_flag:
            theta = math.atan2(reqR[1][0], reqR[0][0])

            y2_aux = math.cos(theta)*pose["y"] + math.sin(theta)*pose["x"]
            x2_aux = -math.sin(theta)*pose["y"] + math.cos(theta)*pose["x"]

            print("ref: ", xyz_ref, "measured: ", xyz, "measured ICP: ", [x2_aux, y2_aux] )

            new_x = []
            new_y = []
            for i in range(len(x_list)): 
                new_lidar = np.array([float(x_list[i]), float(y_list[i]), 0.0])
                new_x.append(new_lidar)
                new_y.append(np.matmul(reqR, new_lidar.transpose()) + reqT)
                
            x_list = new_x
            y_list = new_y

    return x_list, y_list, x_list_ref, y_list_ref, xyz_ref

'''
This function applies the change of referential in 3D
'''
def multmatr(X,Y,T):
    res = []
    res.append( X[0] * Y[0] + X[3] * Y[1] + X[6] * Y[2] - T[0])
    res.append( X[1] * Y[0] + X[4] * Y[1] + X[7] * Y[2] + T[1])
    res.append( X[2] * Y[0] + X[5] * Y[1] + X[8] * Y[2] + T[2])
    return res


'''
This function calculates a centroid
'''
def indxtMean(index,arrays):
    indxSum = np.array([0.0, 0.0 ,0.0])
    for i in range(np.size(index,0)):
        indxSum = np.add(indxSum, np.array(arrays[index[i]]), out = indxSum ,casting = 'unsafe')
    return indxSum/np.size(index,0)

'''
This function computes a fixed index
'''
def indxtfixed(index,arrays):
    T = []
    for i in index:
        T.append(arrays[i])
    return np.asanyarray(T)

'''
Iterated Closest Points (ICP) function
'''
def ICPSVD(fixedX, fixedY, movingX, movingY):
    reqR = np.identity(3) # Return a identity matrix
    reqT = [0.0, 0.0, 0.0] # 
    fixedt = []
    movingt = []
    
    for i in range(len(fixedX)):
        fixedt.append([float(fixedX[i]), float(fixedY[i]), 0])
    
    for i in range(len(movingX)):
        movingt.append([float(movingX[i]), float(movingY[i]), 0])

    moving = np.asarray(movingt)
    fixed = np.asarray(fixedt)

    n = np.size(moving,0) # pas sur
    
    TREE = KDTree(fixed)
    
    accept_flag = False
    for i in range(10):
        distance, index = TREE.query(moving)
        err = np.mean(distance**2)

        if err > 100: # if too big
            reqR= np.zeros([3, 3])
            reqT = np.array([0, 0, 0])
            accept_flag = False
            continue

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
        accept_flag = True

    return accept_flag, reqR, reqT


'''
This function discretises the walls when doing ICP
'''
def get_discretised_walls(walls):
    discretized_walls_x = []
    discretized_walls_y = []
    for wall in walls:
        wall_x = []
        wall_y = []
        for i in range(len(wall['x']) - 1):
            x0, y0 = wall['x'][i], wall['y'][i]
            x1, y1 = wall['x'][i + 1], wall['y'][i + 1]
            length = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
            
            num_steps = int(length * 100)  # converting length to cm
            x_step = (x1 - x0) / (num_steps + 1e-100)
            y_step = (y1 - y0) / (num_steps + 1e-100)
            for j in range(num_steps):
                x_aux = round((x0 + j * x_step)*100)
                y_aux = round((y0 + j * y_step)*100)
                wall_x.append(x_aux)
                wall_y.append(-y_aux)
        discretized_walls_x.append(wall_y)
        discretized_walls_y.append(wall_x)
    return discretized_walls_x[0], discretized_walls_y[0]
