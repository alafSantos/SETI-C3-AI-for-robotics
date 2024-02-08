from flags_file import flags
import numpy as np
from motors_controller import stop, forward, backward, turn_left, turn_right
import time


ready_rotate = False
ready_forward = False
distance_chosen = 0
angle_chosen = 0
t_previous = 0
distance = 0
largest_gap_distance = 0
largest_gap_index = 0
rotation_angle = 0

# Monitor rotation
m_counter = 0
rotation_counter = 0

def lidar_control(lidar):
    # https://f1tenth-coursekit.readthedocs.io/en/latest/assignments/labs/lab4.html
    angle = 0
    point_cloud = lidar.getRangeImage() # a 360-size list

    x_list = []
    y_list = []
    xy_lidar = []

    for point in point_cloud:
        angle += 2*np.pi / lidar.getHorizontalResolution()

        if not (np.pi/2 < angle < (3/2)*np.pi): # and 0.01 < point < 0.2:
            xy = [point*np.sin(angle), point*np.cos(angle)]
            xy_lidar.append(xy)
            
            if xy[0] < 0:
                x_list.append({"left": 100*xy[0]})
                y_list.append({"left": 100*xy[1]})
            else:
                x_list.append({"right": 100*xy[0]})
                y_list.append({"right": 100*xy[1]})

    return xy_lidar, x_list, y_list
    

# Function to calculate distance between two points
def distance(point1, point2):
    return np.sqrt((point2[0] - point1[0])**2 + (point2[1] - point1[1])**2)

# Function to calculate angle between two points
def angle(point1, point2):
    return np.arctan2(point2[1] - point1[1], point2[0] - point1[0])

def find_largest_gap(lidar_data):
    # Initialize variables to store information about the largest gap
    largest_gap_distance = 0
    largest_gap_index = -1

    # Iterate through the points to find the largest gap
    for i in range(len(lidar_data) - 1):
        # Calculate distance between current point and next point
        dist = distance(lidar_data[i], lidar_data[i + 1])
        
        # Update information if the current gap is larger than the one
        if dist > largest_gap_distance:
            largest_gap_distance = dist
            largest_gap_index = i

    rotation_angle = angle(lidar_data[largest_gap_index], lidar_data[largest_gap_index + 1])

    if largest_gap_distance == np.inf:
        largest_gap_distance = 0

    if rotation_angle == np.inf:
        rotation_angle = 0

    return largest_gap_distance, largest_gap_index, rotation_angle



def motor_control_based_on_lidar(lidar_data, motor_left, motor_right, x_lidar_list, y_lidar_list, speed):
    global ready_rotate, ready_forward, distance_chosen, angle_chosen, t_previous, distance, m_counter, m_per_counter
    global rotation_angle, largest_gap_distance, largest_gap_index, rotation_counter

    m_per_counter = speed/2500 # still need to figure this out
    rad_per_counter = (speed/(1.5*9.53))*np.pi/90 # I think this is correct

    precision = 0.85    

    if not ready_rotate and not ready_forward:
        largest_gap_distance, largest_gap_index, rotation_angle = find_largest_gap(lidar_data)
        print("hey 1")
        
        # Print the largest gap distance and its index
        if flags["debug"]:
            print("Largest gap distance:", largest_gap_distance)
            print("Index of the point where the gap starts:", largest_gap_index)
            print("Rotation angle:", rotation_angle)
    
        ready_rotate = True
        ready_forward = True
        m_counter = 0
        rotation_counter = 0
    
    if ready_rotate:
        # Activate motors to initiate rotation
        if rotation_angle > 0:  # Turn left
            turn_left(motor_left, motor_right, speed)
        elif rotation_angle < 0:  # Turn right
            turn_right(motor_left, motor_right, speed)

        # Check if the wheels has traveled the required distance
        traveled_distance = rotation_counter*rad_per_counter
        rotation_counter += 1

        print("distances rot", traveled_distance, abs(rotation_angle + 2*np.pi/3))

        if rotation_angle < 0:
            if abs(traveled_distance) >= abs(rotation_angle + 2*np.pi/3)*precision:
                # Stop both motors
                stop(motor_left, motor_right)
                ready_rotate = False 
        elif abs(traveled_distance) >= abs(rotation_angle - 2*np.pi/3)*precision:
            # Stop both motors
            stop(motor_left, motor_right)
            rotation_counter = 0
            ready_rotate = False    
 
    elif ready_forward :
        # Activate motors to start moving forward    
        forward(motor_left, motor_right, speed)

        # Check if the wheels has traveled the required distance
        traveled_distance = m_counter*m_per_counter
        
        print("distances forw", traveled_distance, largest_gap_distance)
        if abs(traveled_distance) >= abs(largest_gap_distance)*precision + 0.07:
            # Stop both motors
            stop(motor_left, motor_right)
            ready_forward = False  
        m_counter += 1

    else:
        print("hey 4")
        ready_forward = False
        ready_rotate = False
        stop(motor_left, motor_right)


