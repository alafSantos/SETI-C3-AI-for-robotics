'''
Developed by Alaf D. N. SANTOS and Simon BERTHOUMIEUX in the context of the Artificial Intelligence for Robotics course. Master SETI.

tp6 controller (main file)
'''
# Importing the needed libraries
from controller import *

from motors_controller import forward, backward, stop, keyboard_control
from flags_file import flags
from multi_layer import f_activation_sat
from perceptron import get_y, get_s, f_analogique
import numpy as np

if flags["exercice_4"]:
    w11 = 1.0
    w12 = 1.0
    w21 = 1.0
    w22 = -2.0
    w23 = -2.0
    w24 = 1.0

elif flags["exercice_6"]:
    w_fwd = 0.7
    w_back = 0.9
    w_pos = 1.0
    w_neg = 1.0

    W_l = [w_fwd,w_pos,-w_back,-w_neg]
    W_r = [w_fwd,-w_neg,-w_back,w_pos]
    

robot = Supervisor()
keyboard = Keyboard()

timestep = int(robot.getBasicTimeStep())
keyboard.enable(timestep)

motor_left = robot.getDevice("motor.left")
motor_right = robot.getDevice("motor.right")
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))
motor_left.setVelocity(0)
motor_right.setVelocity(0)
node = robot.getFromDef("Thymio")

sensor_left_front = robot.getDevice('prox.horizontal.0')
sensor_center_front = robot.getDevice('prox.horizontal.2')
sensor_right_front = robot.getDevice('prox.horizontal.4')

sensor_left_back = robot.getDevice('prox.horizontal.5')
sensor_right_back = robot.getDevice('prox.horizontal.6')

sensor_left_front.enable(timestep)
sensor_center_front.enable(timestep)
sensor_right_front.enable(timestep)
sensor_left_back.enable(timestep)
sensor_right_back.enable(timestep)

plot = 0
speed_max = 9.53 # max
distance_max = 4095

while (robot.step(timestep) != -1): #Appel d'une etape de simulation
    plot += 1

    if flags["keyboard"]:
        keyboard_control(keyboard, Keyboard, motor_left, motor_right, speed_max)
    else:
        x_lf = sensor_left_front.getValue()/distance_max
        x_cf = sensor_center_front.getValue()/distance_max
        x_rf = sensor_right_front.getValue()/distance_max
        X_f = [1, x_lf, x_cf, x_rf]

        if flags["exercice_4"]:
            s1 = f_activation_sat(np.matrix(x_lf).T, np.matrix(w11))
            s2 = f_activation_sat(np.matrix(x_rf).T, np.matrix(w12))

            w1 = [w21, w23]
            w2 = [w22, w24]
            
            y1 = f_activation_sat(np.matrix([s1,s2]).T, np.matrix(w1).T)
            y2 = f_activation_sat(np.matrix([s1,s2]).T, np.matrix(w2).T)

            motor_left.setVelocity(y1[0]*speed_max)
            motor_right.setVelocity(y2[0]*speed_max)
        
        elif flags["exercice_6"]:
            s_l = get_s(X_f, W_l)
            y_l = f_analogique(s_l)
            s_r = get_s(X_f, W_r)
            y_r = f_analogique(s_r)

            motor_left.setVelocity(y_l*speed_max)
            motor_right.setVelocity(y_r*speed_max)

        