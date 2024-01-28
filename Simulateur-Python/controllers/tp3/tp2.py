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
debug_mode = False # set True if you want to debug
debug_pt3 = False # set True if you want to debug the last part of the TP (undone)

if graph_mode:
    graph1 = graphWalls()
    graph2 = graphWalls()

kinematics = kinematicsFunctions(2.105 * 1e-2, 10.8 * 1e-2) # wheel radius and track width as parameters

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
linear_displacement = 0

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


need_to_rotate = True
arrived = True
remaining_distance = 0
previous_point_counter = 1000
travelled_distance = 0

# This function is called when we aren't in the keyboard mode
def trajectory_update(p1, p2, point_counter, orientation):
    k = kinematicsFunctions(p1[0], p1[1], 0)

    global arrived, need_to_rotate, remaining_distance, travelled_distance

    angle_to_destination, distance_to_destination = k.get_target(p1, p2, orientation)
    
    if distance_to_destination == 0:
        point_counter += 1
        return point_counter

    if debug_pt3:
        print("point: ", point_counter)

    if arrived and need_to_rotate: # nouveau point
        if debug_pt3:
            print("hey 1")
        need_to_rotate = True
        arrived = False
        travelled_distance = 0

    elif not arrived and not need_to_rotate : # go straight
        if debug_pt3:
            print("hey 2")
        motor_left.setVelocity(speed)
        motor_right.setVelocity(speed)
        travelled_distance += linear_displacement
        if debug_pt3:
            print("travelled_distance", travelled_distance)
            print("distance_to_destination", distance_to_destination)

        if  0.99 < abs(travelled_distance/(distance_to_destination + 0.02)) < 1.01:
            arrived = True

    elif not arrived and need_to_rotate: # rotation
        if debug_pt3:
            print("hey 3", angle_to_destination, orientation)

        if angle_to_destination < -1.57:
            need_to_rotate = False
        elif abs(angle_to_destination - orientation) < 0.008:
            motor_left.setVelocity(-speed)
            motor_right.setVelocity(speed)
        elif abs(orientation - angle_to_destination) < 0.008:
            motor_left.setVelocity(speed)
            motor_right.setVelocity(-speed)
        elif orientation != 0:
            if 0.99 < angle_to_destination/orientation < 1.01:
                need_to_rotate = False
        elif angle_to_destination != 0:
            if 0.99 < orientation/angle_to_destination < 1.01:
                need_to_rotate = False

    else: # arrived
        arrived = True
        need_to_rotate = True
        point_counter += 1
    
    return point_counter

while (robot.step(timestep) != -1): #Appel d'une etape de simulation
    t = robot.getTime()
    dt = t - t_previous
        
    vL = motor_left.getVelocity()
    vR = motor_right.getVelocity() 
    
    linear_displacement, pose = kinematics.get_new_pose(vL, vR, dt)
    
    position = node.getPosition() ## x y z 
    orientation = node.getOrientation()
        
    # 90o rotation
    x_list_ref.append(-100*position[0])
    y_list_ref.append(100*position[2])
    
    if plot % 100 == 0:
        if debug_mode:
            print("\n------------------------------------------------------------------------------")
            print("Measured position: ", pose)
            print("Simulated position S: ", position)
            print("Measured theta: ", -math.degrees(pose["theta"]))
            print("Simulated theta: ", math.degrees(math.atan2(orientation[6], orientation[0])))
               
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
            point_counter = trajectory_update(p1, p2, point_counter, pose["theta"])
        else:
            point_counter = 0

    t_previous = t
    plot += 1
        
      
keyboard.disable()