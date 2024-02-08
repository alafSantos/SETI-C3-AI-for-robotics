from flags_file import flags
import numpy as np
from motors_controller import stop, forward, turn_left, turn_right

ready_rotate = False
ready_forward = False

largest_gap_distance = 0
largest_gap_index = 0
rotation_angle = 0

best_point_rotation_angle = 0
best_point_distance = 0

m_counter = 0
rotation_counter = 0

def lidar_control(lidar):
    # https://f1tenth-coursekit.readthedocs.io/en/latest/assignments/labs/lab4.html
    angle = 0
    point_cloud = lidar.getRangeImage() # a 360-size list
    xy_lidar = []
    
    # Separate points into left and right regions
    x_l_list = []
    y_l_list = []
    x_r_list = []
    y_r_list = []
    lidar_list = []
    
    for point in point_cloud:
        xy = [point*np.sin(angle), point*np.cos(angle)]
        
        if not flags["Reactive"]:
            if not (np.pi/2 < angle < (3/2)*np.pi):
                if flags["bubble"]:
                    # Taking only points inside a defined threshold
                    dist = distance(xy, [0,0])

                    if dist < 0.30: # 30 cm
                        xy_lidar.append(xy)
                else:
                    xy_lidar.append(xy)
        else:
            # Assign points to left or right regions based on angle and distance
            if (point < 0.2) and ((2 > angle) or (angle > 4)):
                lidar_list.append(xy)
                if xy[0] > 0:
                    x_r_list.append(xy[0])
                    y_r_list.append(xy[1])
                else:
                    x_l_list.append(xy[0])
                    y_l_list.append(xy[1])

        angle += 2*np.pi / lidar.getHorizontalResolution()

    if flags["Reactive"]:
        xy_lidar = [x_r_list, y_r_list, x_l_list, y_l_list, lidar_list]

    return xy_lidar 
    

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
        
        # Update information if the current gap is larger than the last one
        if dist > largest_gap_distance:
            largest_gap_distance = dist
            largest_gap_index = i

    rotation_angle = angle(lidar_data[largest_gap_index], lidar_data[largest_gap_index + 1])

    # Remove values equal to infinity
    if largest_gap_distance == np.inf:
        largest_gap_distance = 0

    if rotation_angle == np.inf:
        rotation_angle = 0

    if flags["debug"]:
        print("Largest gap distance:", largest_gap_distance)
        print("Index of the point where the gap starts:", largest_gap_index)
        print("Rotation angle:", rotation_angle)

    return largest_gap_distance, largest_gap_index, rotation_angle

def find_best_point(lidar_data, largest_gap_index):
    dist_1 = distance(lidar_data[largest_gap_index], [0, 0])
    dist_2 = distance(lidar_data[largest_gap_index + 1], [0, 0])

    best_dist = 0

    if dist_1 > dist_2:
        best_idx = largest_gap_index
        best_dist = dist_1
    else:
        best_idx = largest_gap_index + 1
        best_dist = dist_2

    rotation_angle = angle(lidar_data[best_idx], [0, 0])

    return best_dist, best_idx, rotation_angle

def find_nearest_lidar_point(lidar_data):
    # Initialize variables to store information about the nearst point
    nearest_lidar_point_index = -1
    nearest_lidar_point_distance = 0

    # Iterate through the points to find the nearest one
    for i in range(len(lidar_data)):
        dist = distance(lidar_data[i], [0, 0])

        # Update information if the current point is closer than the last one
        if dist < nearest_lidar_point_distance:
            nearest_lidar_point_distance = dist
            nearest_lidar_point_index = i

    return nearest_lidar_point_index

def control_motors(motor_left, motor_right, speed, angle):
    # Negative angle, turn left
    if angle < -0.1: 
        turn_left(motor_left, motor_right, speed)
    
    # Positive angle, turn right
    elif angle > 0.1: 
        turn_right(motor_left, motor_right, speed)
    
    # If the angle to target is very close to zero, go forward
    else: 
        forward(motor_left, motor_right, speed)

def motor_control_based_on_lidar(lidar_data, motor_left, motor_right, speed):
    global ready_rotate, ready_forward, m_counter, m_per_counter
    global rotation_angle, largest_gap_distance, largest_gap_index, rotation_counter
    global best_point_rotation_angle, best_point_distance

    if not flags["bubble"] and not flags["Reactive"]:
        m_per_counter = speed/2500 # estimated value
        rad_per_counter = (speed/(1.5*9.53))*np.pi/90 # estimated value
        precision = 0.84    

        if not ready_rotate and not ready_forward:
            largest_gap_distance, largest_gap_index, rotation_angle = find_largest_gap(lidar_data)
            
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

            if flags["debug"]:
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
            
            if flags["debug"]:
                print("distances forw", traveled_distance, largest_gap_distance)

            if abs(traveled_distance) >= abs(largest_gap_distance)*precision + 0.07:
                # Stop both motors
                stop(motor_left, motor_right)
                ready_forward = False  
            m_counter += 1

        else:
            ready_forward = False
            ready_rotate = False
            stop(motor_left, motor_right)

    elif flags["Reactive"]: # Without the rotation + translation
        # Calculate the average position for left and right regions
        p_r = len(lidar_data[0]) // 4
        p_l = 3 * len(lidar_data[2]) // 4

        x_r_avg = sum(lidar_data[0][:p_r]) / p_r
        x_l_avg = sum(lidar_data[2][p_l:]) / (len(lidar_data[2]) - p_l)

        y_r_avg = sum(lidar_data[1][:p_r]) / p_r
        y_l_avg = sum(lidar_data[3][p_l:]) / (len(lidar_data[3]) - p_l)

        # Calculate the central point between left and right regions
        x = (x_r_avg + x_l_avg) / 2
        y = (y_r_avg + y_l_avg) / 2

        # Adjust robot movement based on the angle to the target
        control_motors(motor_left, motor_right, speed, np.arctan2(x, y))
        
 
    else: # Bubble
        m_per_counter = speed/2500 # estimated value
        rad_per_counter = (speed/(1.5*9.53))*np.pi/90 # estimated value

        if not ready_rotate and not ready_forward:
            nearst_point_idx = find_nearest_lidar_point(lidar_data)
        
            # Setting some points around the nearest one to zero
            lidar_data[nearst_point_idx - 1] = [0,0]
            lidar_data[nearst_point_idx] = [0,0]
            lidar_data[nearst_point_idx + 1] = [0,0]

            # Finding the largest gap
            largest_gap_distance, largest_gap_index, rotation_angle = find_largest_gap(lidar_data)

            best_point_distance, best_point_idx, best_point_rotation_angle = find_best_point(lidar_data, largest_gap_index)
            
            if flags["debug"]:
                print("Largest gap distance:", best_point_distance)
                print("Index of the point where the gap starts:", largest_gap_index)
                print("Rotation angle:", best_point_rotation_angle)
        
            ready_rotate = True
            ready_forward = True
            m_counter = 0
            rotation_counter = 0
        
        if ready_rotate:
            # Activate motors to initiate rotation
            if best_point_rotation_angle > 0:  # Turn left
                turn_left(motor_left, motor_right, speed)
            elif best_point_rotation_angle < 0:  # Turn right
                turn_right(motor_left, motor_right, speed)

            # Check if the wheels has traveled the required distance
            traveled_distance = rotation_counter*rad_per_counter
            rotation_counter += 1

            if flags["debug"]:
                print("distances rot", traveled_distance, abs(best_point_rotation_angle + 2*np.pi/3))

            if best_point_rotation_angle < 0:
                if abs(traveled_distance) >= abs(best_point_rotation_angle + 2*np.pi/3):
                    # Stop both motors
                    stop(motor_left, motor_right)
                    ready_rotate = False 
            elif abs(traveled_distance) >= abs(best_point_rotation_angle - 2*np.pi/3):
                # Stop both motors
                stop(motor_left, motor_right)
                rotation_counter = 0
                ready_rotate = False    
    
        elif ready_forward :
            # Activate motors to start moving forward    
            forward(motor_left, motor_right, speed)

            # Check if the wheels has traveled the required distance
            traveled_distance = m_counter*m_per_counter
            
            if flags["debug"]:
                print("distances forw", traveled_distance, best_point_distance)

            if abs(traveled_distance) >= abs(best_point_distance)*precision + 0.07:
                # Stop both motors
                stop(motor_left, motor_right)
                ready_forward = False  
            m_counter += 1

        else:
            ready_forward = False
            ready_rotate = False
            stop(motor_left, motor_right)




