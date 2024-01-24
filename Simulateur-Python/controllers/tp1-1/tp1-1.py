# c:\users\bastien\appdata\local\programs\python\python39\python
import sys,os
sys.path.append('C:\Program Files\Webots\lib\controller\python39')
import math
import time;
from controller import *
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib import collections  as mc
import random
from scipy.spatial import cKDTree as KDTree

robot = Supervisor()

timestep = int(robot.getBasicTimeStep())
print(timestep)

motor_left = robot.getDevice("motor.left");
motor_right = robot.getDevice("motor.right");
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))


##  principales caractéristiques mécaniques du Thymio 
    # length = 112 # mm
    # width = 117 # mm
    # height = 53 # mm
    # weight = 0.25 # kg
    # maxSpeed = 0.2 # m/s
    # maxRotSpeed = 9.53 # rad/s
    
## actionneurs disponibles sur votre robot

## capteurs embarqués
## 1 rad = 57,2957795o

x = 90
print("desired angle: ", x)
state = 0
t = 0
t_tile = 2900
t_rot = math.floor(13.8*x) - 2 # voir apres
print(t_rot)

while (robot.step(timestep) != -1): #Appel d'une étape de simulation
    t += timestep
    if state == 0:
        motor_left.setVelocity(5)
        motor_right.setVelocity(5)
        if not (t % t_tile):
            state = 1
    elif state == 1:
        motor_left.setVelocity(-5)
        motor_right.setVelocity(5)
        if not (t % t_rot):
            state = 0
            t = 0
    else:
        motor_left.setVelocity(0)
        motor_right.setVelocity(0)
        state = 0
        t = 0     
