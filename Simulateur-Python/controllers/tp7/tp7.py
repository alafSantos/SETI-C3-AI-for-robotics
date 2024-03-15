'''
Developed by Alaf D. N. SANTOS and Simon BERTHOUMIEUX in the context of the Artificial Intelligence for Robotics course. Master SETI.

tp7 controller (main file)
'''
# Importing the needed libraries
from controller import *

from motors_controller import keyboard_control
from flags_file import flags
import numpy as np
import h5py
import pickle

if flags["exercice_8"]:
    w_fwd = 0.7
    w_back = 0.9
    w_pos = 1.0
    w_neg = 1.0
    
    W_l = [w_fwd,w_pos,-w_back,-w_neg]
    W_r = [w_fwd,-w_neg,-w_back,w_pos]

    def f_activation_sat(x, w):
        s_vec = np.dot(x,w)
        y_vec = []
        for s in s_vec:
            if s < -1:
                y = -1
            elif s > 1:
                y = 1
            else:
                y = float(s[0])
            y_vec.append(y)

        return y_vec

# Récupération du model
if flags["exercice_10"]:
    with open('ai_controller_model_hyper_prox.model', 'rb') as f:
        controller = pickle.load(f)

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
sensor_left2_front = robot.getDevice('prox.horizontal.1')
sensor_center_front = robot.getDevice('prox.horizontal.2')
sensor_right2_front = robot.getDevice('prox.horizontal.3')
sensor_right_front = robot.getDevice('prox.horizontal.4')

sensor_left_back = robot.getDevice('prox.horizontal.5')
sensor_right_back = robot.getDevice('prox.horizontal.6')

sensor_left_front.enable(timestep)
sensor_left2_front.enable(timestep)
sensor_center_front.enable(timestep)
sensor_right_front.enable(timestep)
sensor_right2_front.enable(timestep)

sensor_left_back.enable(timestep)
sensor_right_back.enable(timestep)

speed_max = 9.53 # max
distance_max = 4095

proximeters_list = []
speed_list = []

saved = False

while (robot.step(timestep) != -1): #Appel d'une etape de simulation

    if flags["keyboard"]:
        keyboard_control(keyboard, Keyboard, motor_left, motor_right, speed_max)
    else:
        key=keyboard.getKey()

        x_lf = sensor_left_front.getValue()/distance_max
        x_l2f = sensor_left2_front.getValue()/distance_max
        x_cf = sensor_center_front.getValue()/distance_max
        x_rf = sensor_right_front.getValue()/distance_max
        x_r2f = sensor_right2_front.getValue()/distance_max

        x_lb = sensor_left_back.getValue()/distance_max
        x_rb = sensor_right_back.getValue()/distance_max

        X_f = [1, x_lf, x_cf, x_rf]

        if flags["exercice_8"]:

            y_l = f_activation_sat(np.matrix(X_f), np.matrix(W_l).T)
            y_r = f_activation_sat(np.matrix(X_f), np.matrix(W_r).T)

            sl = y_l[0]*speed_max
            sr = y_r[0]*speed_max

            motor_left.setVelocity(sl)
            motor_right.setVelocity(sr)

            speed_list.append([sl, sr])
            proximeters_list.append([x_lf, x_l2f, x_cf, x_rf, x_r2f, x_lb, x_rb])
            
            if (key==Keyboard.DOWN) and not saved:
                print("Saving dataset...")
                # Open an HDF5 file for writing
                with h5py.File("datasets/dataset_webots.hdf5", "w") as f:
                    speed_array = np.array(speed_list)
                    proximeters_array = np.array(proximeters_list)

                    # Create the main dataset (can be empty or contain additional data)
                    speed_dataset = f.create_dataset('thymio_speed', data=speed_array)
                    proximeters_dataset = f.create_dataset('thymio_prox', data=proximeters_array)

                    # Close the HDF5 file
                    speed_list = []
                    proximeters_list = []
                    saved = True
                    f.close()

        if flags["exercice_10"]:
            s=controller.predict([[x_lf, x_l2f, x_cf, x_rf, x_r2f, x_lb, x_rb]])
            s=np.clip(s, -1, 1)
            motor_left.setVelocity(s[0][0]*speed_max)
            motor_right.setVelocity(s[0][1]*speed_max)