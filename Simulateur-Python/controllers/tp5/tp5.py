'''
Developed by Alaf D. N. SANTOS and Simon BERTHOMIEUX in the context of the Artificial Intelligence for Robotics course. Master SETI.

tp5 controller (main file)
'''
# Importing the needed libraries
from controller import *

from motors_controller import forward, stop
from perceptron import get_y, get_s, f_analogique
from flags_file import flags

w_and = [-1.5, 1.0, 1.0]
w_or = [-0.5, 1.0, 1.0]
w_detec=[0.0,1.0,1.0]

# Partie 1
# w_back = 1.0
# w_pos = 0.75
# w_neg = 0.75
# w_fwd = 0.50

# Partie 2 - Suivie
w_back = 0.75
w_pos = -0.25
w_neg = -0.25
w_fwd = 0.75

W_l = [w_fwd,w_pos,-w_back,-w_neg]
W_r = [w_fwd,-w_neg,-w_back,w_pos]

robot = Supervisor()

timestep = int(robot.getBasicTimeStep())

motor_left = robot.getDevice("motor.left")
motor_right = robot.getDevice("motor.right")
motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))
motor_left.setVelocity(0)
motor_right.setVelocity(0)
node = robot.getFromDef("Thymio")

s_lf = robot.getDevice('prox.horizontal.0')
s_cf = robot.getDevice('prox.horizontal.2')
s_rf = robot.getDevice('prox.horizontal.4')

s_lb = robot.getDevice('prox.horizontal.5')
s_rb = robot.getDevice('prox.horizontal.6')

s_lf.enable(timestep)
s_cf.enable(timestep)
s_rf.enable(timestep)
s_lb.enable(timestep)
s_rb.enable(timestep)

plot = 0
speed_max = 9.53 # max
distance_max = 4095

while (robot.step(timestep) != -1): #Appel d'une etape de simulation
    plot += 1

    x_b1 = s_lb.getValue()/distance_max
    x_b2 = s_rb.getValue()/distance_max
    X_b =[1, x_b1, x_b2]

    x_lf = s_lf.getValue()/distance_max
    x_cf = s_cf.getValue()/distance_max
    x_rf = s_rf.getValue()/distance_max
    X_f = [1, x_lf, x_cf, x_rf]

    if flags["exercice_2"]:
        s = get_s(X_b, w_detec)
        y = get_y(s)
        print("s, y = ", s, y)

        if y == 1:
            forward(motor_left, motor_right, 4)
        else:
            stop(motor_left, motor_right)

    if flags["exercice_3_1"]:
        s = get_s([x_cf], [-1])
        y = f_analogique(s)
        forward(motor_left, motor_right, y*speed_max)

    if flags["exercice_3_2"]:
        s_l = get_s(X_f, W_l)
        y_l = f_analogique(s_l)
        s_r = get_s(X_f, W_r)
        y_r = f_analogique(s_r)

        motor_left.setVelocity(y_l*speed_max)
        motor_right.setVelocity(y_r*speed_max)