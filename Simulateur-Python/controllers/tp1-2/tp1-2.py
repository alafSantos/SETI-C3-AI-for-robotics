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
from controller import Keyboard

print("Init...")

robot = Supervisor()

timestep = int(robot.getBasicTimeStep())

keyboard=Keyboard()
keyboard.enable(timestep)

motor_left = robot.getDevice("motor.left");
motor_right = robot.getDevice("motor.right");
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))


while (robot.step(timestep) != -1): #Appel d'une étape de simulation
    key=keyboard.getKey()
    
    if (key==Keyboard.UP):
        motor_left.setVelocity(5)
        motor_right.setVelocity(5)
        
    elif (key==Keyboard.DOWN):
        motor_left.setVelocity(-5)
        motor_right.setVelocity(-5)
    
    elif(key==Keyboard.LEFT):
        motor_left.setVelocity(-5)
        motor_right.setVelocity(5)
    
    elif(key==Keyboard.RIGHT):
        motor_left.setVelocity(5)
        motor_right.setVelocity(-5)

    else:
        motor_left.setVelocity(0)
        motor_right.setVelocity(0)
      

keyboard.disable()
