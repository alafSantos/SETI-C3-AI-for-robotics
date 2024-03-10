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

elif flags["exercice_6_ref"]:
    w_fwd = 0.7
    w_back = 0.9
    w_pos = 1.0
    w_neg = 1.0
    

    W_l = [w_fwd,w_pos,-w_back,-w_neg]
    W_r = [w_fwd,-w_neg,-w_back,w_pos]

elif flags["exercice_6"]:
    w_fwd = 0.7
    w_back = 0.9
    w_pos = 1.0
    w_neg = 1.0
    w_rec = 0.5

    x_rec_l=0.0
    x_rec_r=0.0

    W_l = [w_fwd,w_pos,-w_back,-w_neg,w_rec]
    W_r = [w_fwd,-w_neg,-w_back,w_pos,w_rec]
    

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
sensor_left_center_front = robot.getDevice('prox.horizontal.1')
sensor_center_front = robot.getDevice('prox.horizontal.2')
sensor_right_center_front = robot.getDevice('prox.horizontal.3')
sensor_right_front = robot.getDevice('prox.horizontal.4')

sensor_left_back = robot.getDevice('prox.horizontal.5')
sensor_right_back = robot.getDevice('prox.horizontal.6')

sensor_left_front.enable(timestep)
sensor_left_center_front.enable(timestep)
sensor_center_front.enable(timestep)
sensor_right_center_front.enable(timestep)
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
        x_lcf = sensor_left_center_front.getValue()/distance_max
        x_cf = sensor_center_front.getValue()/distance_max
        x_rcf = sensor_right_center_front.getValue()/distance_max
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


        elif flags["exercice_6_ref"]:
            y_l = f_activation_sat(np.matrix(X_f).T, np.matrix(W_l).T)
            y_r = f_activation_sat(np.matrix(X_f).T, np.matrix(W_r).T)


            motor_left.setVelocity(y_l[0]*speed_max)
            motor_right.setVelocity(y_r[0]*speed_max)
        
        elif flags["exercice_6"]:
            X_f_l = [1, x_lf, x_cf, x_rf,x_rec_l]
            X_f_r = [1, x_lf, x_cf, x_rf,x_rec_r]
            y_l = f_activation_sat(np.matrix(X_f_l), np.matrix(W_l).T)
            y_r = f_activation_sat(np.matrix(X_f_r), np.matrix(W_r).T)

            x_rec_l=y_l[0]
            x_rec_r=y_r[0]

            motor_left.setVelocity(y_l[0]*speed_max)
            motor_right.setVelocity(y_r[0]*speed_max)
            
        elif flags["exercice_7"]:
            y_1 = f_activation_sat(np.matrix([x_lf,x_lcf]), np.matrix([4,-4]).T)
            y_2 = f_activation_sat(np.matrix([x_lf,x_lcf,x_cf]), np.matrix([-2,4,-2]).T)
            y_3 = f_activation_sat(np.matrix([x_lcf,x_cf,x_rcf]), np.matrix([-2,4,-2]).T)
            y_4 = f_activation_sat(np.matrix([x_cf,x_rcf,x_rf]), np.matrix([-2,4,-2]).T)
            y_5 = f_activation_sat(np.matrix([x_rcf,x_rf]), np.matrix([-4,4]).T)

            print(y_1[0],y_2[0],y_3[0],y_4[0],y_5[0])
        
        
        elif flags["exercice_8"]:
            y_1 = f_activation_sat(np.matrix([x_lf,x_lcf]), np.matrix([4,-4]).T)
            y_2 = f_activation_sat(np.matrix([x_lf,x_lcf,x_cf]), np.matrix([-2,4,-2]).T)
            y_3 = f_activation_sat(np.matrix([x_lcf,x_cf,x_rcf]), np.matrix([-2,4,-2]).T)
            y_4 = f_activation_sat(np.matrix([x_cf,x_rcf,x_rf]), np.matrix([-2,4,-2]).T)
            y_5 = f_activation_sat(np.matrix([x_rcf,x_rf]), np.matrix([-4,4]).T)

            y_6 = f_activation_sat(np.matrix([y_1[0],y_2[0]]), np.matrix([-0.9,-1.1]).T)
            y_7 = f_activation_sat(np.matrix([y_3[0]]), np.matrix([-1]).T)
            y_8 = f_activation_sat(np.matrix([y_4[0],y_5[0]]), np.matrix([-1.1,-0.9]).T)

            y_l = f_activation_sat(np.matrix([y_6[0],y_7[0]]), np.matrix([3.0,1.0]).T)
            y_r = f_activation_sat(np.matrix([y_7[0],y_8[0]]), np.matrix([1.0,3.0]).T)

            motor_left.setVelocity(y_l[0]*speed_max)
            motor_right.setVelocity(y_r[0]*speed_max)
            
            #print(y_1[0],y_2[0],y_3[0],y_4[0],y_5[0])
            #print(y_l[0],y_r[0])