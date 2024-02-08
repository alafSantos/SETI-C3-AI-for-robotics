'''
Developed by Alaf DO NASCIMENTO SANTOS in the context of the Artificial Intelligence for Robotics course. Master SETI.

tp4 controller (main file)
'''
# Importing the needed libraries
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

plot = 0
speed = 9.53

lidar = robot.getDevice('lidar')
lidar.enable(timestep)
lidar.enablePointCloud()

while (robot.step(timestep) != -1): #Appel d'une etape de simulation
    plot += 1

    xy_lidar_list = lidar_control(lidar)

    if plot % 50 == 0:
        plot = 0
        if flags["debug"]:
            print("\n------------------------------------------------------------------------------")
            # print("Lidar: ", xy_lidar_list)

        if flags["graphics"]:
            if flags["reactive"]:
                graph.simple_plot([point[0] for point in xy_lidar_list[-1]], [point[1] for point in xy_lidar_list[-1]]) # LIDAR
            else:    
                graph.simple_plot([point[0] for point in xy_lidar_list], [point[1] for point in xy_lidar_list]) # LIDAR

    if flags["keyboard"]:
        keyboard_control(keyboard, Keyboard, motor_left, motor_right, speed)
    else:
        motor_control_based_on_lidar(xy_lidar_list, motor_left, motor_right, speed)
      
keyboard.disable()
