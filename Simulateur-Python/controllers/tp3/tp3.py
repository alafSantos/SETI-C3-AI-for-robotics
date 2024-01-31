'''
Developed by Alaf DO NASCIMENTO SANTOS in the context of the Artificial Intelligence for Robotics course. Master SETI.

tp3 controller (main file)
'''
# Importing the needed libraries
import math
from controller import *

import functions
from graph_walls import graphWalls
from kinematics_func import kinematicsFunctions

keyboard_mode = True # set True if you want to control the robot with your keyboard (UP, DOWN, LEFT, RIGHT)
graph_mode = False # set True if you want to see the 2D matplotlib graphic representation of the system
debug_mode = False # set True if you want to debug

if graph_mode:
    graph1 = graphWalls()
    graph2 = graphWalls()

kinematics = kinematicsFunctions(2.105 * 1e-2, 10.6 * 1e-2) # wheel radius and track width as parameters

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

t = 0
plot = 0
speed = 5

x_list = []
y_list = []
x_list_ref = []
y_list_ref = []

lidar = robot.getDevice('lidar')
lidar.enable(timestep)
lidar.enablePointCloud()

dt = 0
t_previous = 0
xyz_ref = []
trajectory_x = []
trajectory_y = []
trajectory_x_ref = []
trajectory_y_ref = []

while (robot.step(timestep) != -1): #Appel d'une etape de simulation
    key=keyboard.getKey()

    plot += 1
    t = robot.getTime()
    vL = motor_left.getVelocity()
    vR = motor_right.getVelocity()

    dt = t - t_previous

    linear_displacement, pose = kinematics.get_new_pose(vL, vR, dt)
    x_list, y_list, x_list_ref, y_list_ref, xyz_ref = functions.lidar_control(lidar, node, pose, kinematics)

    trajectory_x.append(-100*pose['x'])
    trajectory_y.append(100*pose['y'])
    trajectory_x_ref.append(-100*xyz_ref[0])
    trajectory_y_ref.append(100*xyz_ref[2])
    
    if plot % 100 == 0:
        plot = 0
        if debug_mode:
            print("\n------------------------------------------------------------------------------")
            print("Measured position: ", pose)
            print("Simulated position S: ", position)
            print("Measured theta: ", -math.degrees(pose["theta"]))
            print("Simulated theta: ", math.degrees(math.atan2(orientation[6], orientation[0])))

        if graph_mode:
            graph1.plot_robot(x_list, y_list, 'red') # LIDAR
            graph1.plot_robot(trajectory_x, trajectory_y, 'black')

            graph2.plot_robot(x_list_ref, y_list_ref, 'blue') # LIDAR
            graph2.plot_robot(trajectory_x_ref, trajectory_y_ref, 'black')

    functions.keyboard_control(key, Keyboard, motor_left, motor_right, speed)
    t_previous = t
      
keyboard.disable()