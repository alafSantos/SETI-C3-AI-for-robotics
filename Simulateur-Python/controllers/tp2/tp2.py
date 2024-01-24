from controller import *
from controller import Keyboard

from graph_walls import graphWalls # a class I wrote
from kinematics_func import kinematicsFunctions # a class I wrote

walls = graphWalls()
kinematics = kinematicsFunctions()

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

pose = {'x': -0.5, 'y': 0.125, 'z': 0, 'theta': 0}

t = 0
t_previous = 0
dt = 0
plot = 0
speed = 5

node = robot.getFromDef("Thymio");

while (robot.step(timestep) != -1): #Appel d'une etape de simulation
    t = robot.getTime()
    dt = t - t_previous

    key=keyboard.getKey()
        
    vL = motor_left.getVelocity()
    vR = motor_right.getVelocity() 
    
    pose = kinematics.get_pose(vL, vR, dt)    
    
    if plot % 100 == 0:
        position = node.getPosition() ## x y z 
        orientation = node.getOrientation()

        print("\n------------------------------------------------------------------------------")
        print("position C: ", pose)
        print("position S: ", position)    
    

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
        
    t_previous = t
    plot += 1
        
      
keyboard.disable()