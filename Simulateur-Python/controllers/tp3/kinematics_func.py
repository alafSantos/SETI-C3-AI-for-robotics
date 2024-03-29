'''
Developed by Alaf DO NASCIMENTO SANTOS in the context of the Artificial Intelligence for Robotics course. Master SETI.

kinematicsFunctions class - This class helps in computing the robot kinematics parameters
'''
import numpy as np
import math

class kinematicsFunctions():
    '''
    Class constructor
    '''
    def __init__(self, radius=2.105 * 1e-2, track=10.8 * 1e-2, x=0.125, y=-0.5, orientation=0):
        # Initial Pose
        self.robot_pose = {'x': x, 'y': y, 'theta': orientation}

        # Physical information of the robot
        self.wheel_radius = radius # empirical value
        self.track_width = track # empirical value
        
        # Trajectory variables
        self.x_list = []
        self.y_list = []

        # Labyrinth trajectory
        self.labyrinth_trajectory = [
            {'x': -0.500, 'y': 0.125},
            {'x': -0.150, 'y': 0.125},
            {'x': -0.150, 'y': 0.900},
            {'x': 0.574, 'y': 0.574},
            {'x': 0.584, 'y': 0.409},
            {'x': 0.187, 'y': 0.402},
            {'x': 0.134, 'y': -0.556},
            {'x': -0.083, 'y': -0.564},
            {'x': -0.100, 'y': -0.176},
            {'x': -0.569, 'y': -0.134},
            {'x': -0.572, 'y': 0.079},
            {'x': -0.500, 'y': 0.125}
        ]

    def set_pose(self, x, y, theta):
        self.robot_pose["x"] = x
        self.robot_pose["y"] = y
        self.robot_pose["theta"] = theta

    def get_new_pose(self, left_wheel_speed, right_wheel_speed, dt):
        # Convert wheel speeds from rad/s to m/s
        right_wheel_speed_m = self.wheel_radius * right_wheel_speed
        left_wheel_speed_m = self.wheel_radius * left_wheel_speed

        # Distance travelled by the right and left wheel
        right_wheel_displacement = right_wheel_speed_m * dt
        left_wheel_displacement = left_wheel_speed_m * dt

        # Calculate longitudinal displacement
        linear_displacement = (right_wheel_displacement + left_wheel_displacement) / 2

        # Calculate rotational displacement
        angular_displacement = (right_wheel_displacement - left_wheel_displacement) / self.track_width

        self.robot_pose['x'] += linear_displacement * np.sin(self.robot_pose['theta'] + angular_displacement/2)
        self.robot_pose['y'] += linear_displacement * np.cos(self.robot_pose['theta'] + angular_displacement/2)
        self.robot_pose['theta'] += angular_displacement

        # Update traveled path
        self.x_list.append(-100*self.robot_pose['x'])
        self.y_list.append(100*self.robot_pose['y'])

        return linear_displacement, self.robot_pose

    def rotation_matrix(self, angle):
        # Computing the rotation matrix (about the X-axis)
        rotation_mat = [np.cos(angle), 0, np.sin(angle), 0, 1, 0, -np.sin(angle), 0, np.cos(angle)]
        return rotation_mat

    # Get labyrinth_trajectory parameter
    def get_labyrinth_trajectory(self):
        return self.labyrinth_trajectory
    
    # Get robot_pose parameter
    def get_pose(self):
        return self.robot_pose

    # Get x_list parameter
    def get_x_list(self):
        return self.x_list

    # Get y_list parameter
    def get_y_list(self):
        return self.y_list
    

    def get_new_point(self, x2, y2, theta):
        # Target rotation
        y2_aux = math.cos(theta)*y2 + math.sin(theta)*x2
        x2_aux = -math.sin(theta)*y2 + math.cos(theta)*x2

        return x2_aux, y2_aux
    

    def get_target(self, p1, p2, theta):
        # Separete the values
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]

        # Target rotation
        x2_aux, y2_aux = self.get_new_point(x2, y2, theta)
        x2_aux -= x1
        
        if x2 > 0 and x1 > 0:
            if y2 > 0 and y1 < 0 :
                x2_aux += 2*x1        

        y2_aux -= y1 

        angle = math.atan2(y2_aux, x2_aux) - math.pi/2
        distance = math.sqrt(y2_aux**2 + x2_aux**2)

        return angle, distance
        