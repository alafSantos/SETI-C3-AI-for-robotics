'''
Developed by Alaf DO NASCIMENTO SANTOS in the context of the Artificial Intelligence for Robotics course. Master SETI.

tp5 controller (main file)
'''
# Importing the needed libraries
from controller import *

from graph_walls import graphWalls
from motors_controller import keyboard_control, forward, backward, turn_left, turn_right, stop
from perceptron import get_y, get_s
from flags_file import flags

# I need to remember to map the sensors output to 0s and 1s
w0_and = -1.0
w1_and = 0.1
w2_and = 0.9

w0_or = -1.0
w1_or = 1.0
w2_or = 1.0

if flags["graphics"]:
    graph = graphWalls()

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

plot = 0
speed = 9.53

lidar = robot.getDevice('lidar')
lidar.enable(timestep)
lidar.enablePointCloud()

while (robot.step(timestep) != -1): #Appel d'une etape de simulation
    plot += 1

    # Here I have to read the distance sensors
    x1 = 1
    x2 = 0

    if plot % 50 == 0:
        plot = 0
        if flags["debug"]:
            print("\n------------------------------------------------------------------------------")
            # print("Lidar: ", xy_lidar_list)

        # if flags["graphics"]:
        #     if flags["reactive"]:
        #         graph.simple_plot([point[0] for point in xy_lidar_list[-1]], [point[1] for point in xy_lidar_list[-1]]) # LIDAR
        #     else:    
        #         graph.simple_plot([point[0] for point in xy_lidar_list], [point[1] for point in xy_lidar_list]) # LIDAR

    if flags["keyboard"]:
        keyboard_control(keyboard, Keyboard, motor_left, motor_right, speed)
    else:
        s = get_s(x1, x2, w0_and, w1_and, w2_and)
        y = get_y(s)

        if y == 1:
            forward(motor_left, motor_right, speed)
keyboard.disable()
