'''
Developed by Alaf DO NASCIMENTO SANTOS in the context of the Artificial Intelligence for Robotics course. Master SETI.

tp4 controller (main file)
'''
# Importing the needed libraries
import math
from controller import *

from graph_walls import graphWalls
from lidar_controller import lidar_control, motor_control_based_on_lidar
from motors_controller import keyboard_control

from flags_file import flags

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

t = 0
plot = 0
speed = 9.53

x_list_LIDAR = []
y_list_LIDAR = []
x_list_ref = []
y_list_ref = []

lidar = robot.getDevice('lidar')
lidar.enable(timestep)
lidar.enablePointCloud()

dt = 0
xyz_ref = []
trajectory_x = []
trajectory_y = []
trajectory_x_ref = []
trajectory_y_ref = []

xyz_init = node.getPosition()
theta_init = node.getOrientation()
theta_init = math.atan2(theta_init[6], theta_init[0])

while (robot.step(timestep) != -1): #Appel d'une etape de simulation
    plot += 1

    xy_lidar_list, x_lidar_list, y_lidar_list = lidar_control(lidar)

    if plot % 100 == 0:
        plot = 0
        if flags["debug"]:
            print("\n------------------------------------------------------------------------------")
            print("Lidar: ", xy_lidar_list)

        if flags["graphics"]:
            graph.simple_plot([point[0] for point in xy_lidar_list], [point[1] for point in xy_lidar_list]) # LIDAR
            x_lidar_list = []
            y_lidar_list = []

            cpt_lidar = 25


            #graph.plot_robot(trajectory_x_ref, trajectory_y_ref, 'green')

    if flags["keyboard"]:
        keyboard_control(keyboard, Keyboard, motor_left, motor_right, speed)
    else:
        motor_control_based_on_lidar(xy_lidar_list, motor_left, motor_right, x_lidar_list, y_lidar_list, speed)
      
keyboard.disable()