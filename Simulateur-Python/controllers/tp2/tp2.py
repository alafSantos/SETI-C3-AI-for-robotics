'''
Developed by Alaf DO NASCIMENTO SANTOS in the context of the Artificial Intelligence for Robotics course. Master SETI.

tp2 controller (main file)
'''
# Importing the needed libraries
import math
from controller import *
from controller import Keyboard
from graph_walls import graphWalls
from kinematics_func import kinematicsFunctions

keyboard_mode = False # set True if you want to control the robot with your keyboard (UP, DOWN, LEFT, RIGHT)
graph_mode = False # set True if you want to see the 2D matplotlib graphic representation of the system

if graph_mode:
    graph1 = graphWalls()
    graph2 = graphWalls()

kinematics = kinematicsFunctions(2.1 * 1e-2, 10.8 * 1e-2) # wheel radius and track width as parameters

robot = Supervisor()
keyboard = Keyboard()

timestep = int(robot.getBasicTimeStep())

keyboard.enable(timestep)

motor_left = robot.getDevice("motor.left");
motor_right = robot.getDevice("motor.right");

motor_left.setPosition(float('inf'))
motor_right.setPosition(float('inf'))

motor_left.setVelocity(0)
motor_right.setVelocity(0)

node = robot.getFromDef("Thymio")

pose = {'x': 0.125, 'y': -0.5, 'z': 0, 'theta': 0}

t = 0
t_previous = 0
dt = 0
plot = 0
speed = 5
point_counter = 0

x_list_ref = []
y_list_ref = []

trajectory = kinematics.get_labyrinth_trajectory()
trajectory_x = []
trajectory_y = []

for p in trajectory:
    trajectory_x.append(-100*p['y'])
    trajectory_y.append(100*p['x'])

# This function is called when we are in the keyboard mode
def keyboard_control():
    key=keyboard.getKey()
    
    if (key==Keyboard.UP):
        motor_left.setVelocity(speed)
        motor_right.setVelocity(speed)
        
    elif (key==Keyboard.DOWN):
        motor_left.setVelocity(-speed)
        motor_right.setVelocity(-speed)
    
    elif(key==Keyboard.LEFT):
        motor_left.setVelocity(-speed)
        motor_right.setVelocity(speed)
    
    elif(key==Keyboard.RIGHT):
        motor_left.setVelocity(speed)
        motor_right.setVelocity(-speed)

    else:
        motor_left.setVelocity(0)
        motor_right.setVelocity(0)

# This function is called when we aren't in the keyboard mode
def trajectory_update(theta_pose, p1, p2, point_counter):
    k = kinematicsFunctions(p1[0], p1[1], 0)

    angle_to_destination = k.angle_between_vectors(p1, p2)

    k.rotate(angle_to_destination)

    theta = math.degrees(angle_to_destination)

    print(math.cos(angle_to_destination), math.cos(theta_pose))

    if -1 < theta < 1 and (0.8 < abs(math.cos(theta_pose)/math.cos(angle_to_destination)) < 1.2) : # go straight
        motor_left.setVelocity(speed)
        motor_right.setVelocity(speed)

    elif -1 < theta < 180:
        motor_left.setVelocity(-speed)
        motor_right.setVelocity(speed)
    else:
        print("helloo")
        motor_left.setVelocity(0)
        motor_right.setVelocity(0)
        point_counter += 1


    k.rotate(angle_to_destination)

    k.translate(p1, p2)
    
    return point_counter

while (robot.step(timestep) != -1): #Appel d'une etape de simulation
    t = robot.getTime()
    dt = t - t_previous
        
    vL = motor_left.getVelocity()
    vR = motor_right.getVelocity() 
    
    pose = kinematics.get_new_pose(vL, vR, dt)
    
    position = node.getPosition() ## x y z 
    orientation = node.getOrientation()
        
    # 90o rotation
    x_list_ref.append(-100*position[0])
    y_list_ref.append(100*position[2])
    
    if plot % 100 == 0:
        # print("\n------------------------------------------------------------------------------")
        # print("Measured position: ", pose)
        # print("Simulated position S: ", position)
        # print("Measured theta: ", -math.degrees(pose["theta"]))
        # print("Simulated theta: ", math.degrees(math.atan2(orientation[6], orientation[0])))
               
        if graph_mode:
            graph1.plot_robot(x_list_ref, y_list_ref, 'blue')
            graph2.plot_robot(kinematics.get_x_list(), kinematics.get_y_list(), 'red')
            graph1.plot_robot(trajectory_x, trajectory_y, 'black', True)
            graph2.plot_robot(trajectory_x, trajectory_y, 'black', True)

    if keyboard_mode:
        keyboard_control()
    elif plot % 30:
        if (point_counter < len(trajectory)):
            p1 = [pose["y"], pose["x"]]
            p2 = [trajectory[point_counter]['x'], trajectory[point_counter]['y']]
            point_counter = trajectory_update(pose["theta"], p1, p2, point_counter)
        else:
            point_counter = 0

    t_previous = t
    plot += 1
        
      
keyboard.disable()