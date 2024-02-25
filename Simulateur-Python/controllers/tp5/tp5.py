'''
Developed by Alaf D. N. SANTOS and Simon BERTHOMIEUX in the context of the Artificial Intelligence for Robotics course. Master SETI.

tp5 controller (main file)
'''
# Importing the needed libraries
from controller import *

from motors_controller import forward, backward, stop, keyboard_control
from perceptron import get_y, get_s, f_analogique
from flags_file import flags

w_and = [-1.5, 1.0, 1.0]
w_or = [-0.5, 1.0, 1.0]

# Partie 1
if flags["exercice_3_1"]:
    w_fwd = 0.7
    w_back = 0.9
    w_pos = 1.0
    w_neg = 1.0

# Partie 2 - Suivie
elif flags["exercice_3_2"]:
    w_fwd = 1.0
    w_back = 1.0
    w_pos = -0.5
    w_neg = -0.5

if flags["exercice_3_1"] or flags["exercice_3_2"]:
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
        x_b1 = int(sensor_left_back.getValue()/distance_max > 0.01)
        x_b2 = int(sensor_right_back.getValue()/distance_max > 0.01)
        X_b =[1, x_b1, x_b2]

        x_lf = sensor_left_front.getValue()/distance_max
        x_cf = sensor_center_front.getValue()/distance_max
        x_rf = sensor_right_front.getValue()/distance_max
        X_f = [1, x_lf, x_cf, x_rf]

        if flags["exercice_2"]:
            s = get_s(X_b, w_and)
            y = get_y(s)

            if flags["debug"]:
                print("X_b, s, y = ", X_b, s, y)

            if y == 1:
                forward(motor_left, motor_right, 4)
            else:
                stop(motor_left, motor_right)

        elif flags["exercice_3_0_1"]:
            s = get_s([x_cf], [1])
            y = f_analogique(s)
            backward(motor_left, motor_right, y*speed_max)

        elif flags["exercice_3_0_2"]:
            s = get_s([x_lf, x_rf], [0.5, 1])
            y = f_analogique(s)
            forward(motor_left, motor_right, y*speed_max)

        elif flags["exercice_3_1"] or flags["exercice_3_2"]:
            s_l = get_s(X_f, W_l)
            y_l = f_analogique(s_l)
            s_r = get_s(X_f, W_r)
            y_r = f_analogique(s_r)

            motor_left.setVelocity(y_l*speed_max)
            motor_right.setVelocity(y_r*speed_max)