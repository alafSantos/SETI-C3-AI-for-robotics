import sys,os
import math
import time;
from controller import *
import matplotlib.pyplot as plt
import numpy as np
# import matplotlib
# from matplotlib import collections  as mc
import random
from scipy.spatial import cKDTree as KDTree

robot = Supervisor()

timestep = int(robot.getBasicTimeStep())

motor_left = robot.getDevice("motor.left");
motor_right = robot.getDevice("motor.right");
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))

while (robot.step(timestep) != -1): #Appel d'une étape de simulation
    motor_left.setVelocity(-5)
    motor_right.setVelocity(5)