'''
Developed by Alaf D. N. SANTOS and Simon BERTHOUMIEUX in the context of the Artificial Intelligence for Robotics course. Master SETI.

tp7 controller (main file)
'''
# Importing the needed libraries
from controller import *

from motors_controller import forward, backward, stop, keyboard_control
from flags_file import flags
from perceptron import operateurXOR
import numpy as np
    

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

        if flags["exercice_8"]:
            print("starting")
        