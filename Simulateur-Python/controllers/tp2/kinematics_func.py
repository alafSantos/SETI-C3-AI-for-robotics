'''
Developed by Alaf DO NASCIMENTO SANTOS in the context of the Artificial Intelligence for Robotics course. Master SETI.

kinematicsFunctions class - This class helps in computing the robot kinematics parameters
'''

import numpy as np
import math

class kinematicsFunctions():
    def __init__(self, radius=2.1 * 1e-2, track=10.8 * 1e-2, x=0.125, y=-0.5, orientation=0):
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
            {'x': -0.150, 'y': 0.574},
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

    def get_displacements(self, left_wheel_speed, right_wheel_speed, dt):
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
        
        return linear_displacement, angular_displacement


    def get_new_pose(self, left_wheel_speed, right_wheel_speed, dt):
        # Calculate linear and angular displacements
        linear_displacement, delta_theta = self.get_displacements(left_wheel_speed, right_wheel_speed, dt)

        self.robot_pose['x'] += linear_displacement * np.sin(self.robot_pose['theta'] + delta_theta/2)
        self.robot_pose['y'] += linear_displacement * np.cos(self.robot_pose['theta'] + delta_theta/2)
        self.robot_pose['theta'] += delta_theta

        # Update traveled path
        self.x_list.append(-100*self.robot_pose['x'])
        self.y_list.append(100*self.robot_pose['y'])

        return self.robot_pose

    def angle_between_vectors(self, p1, p2):
        # Separete the values
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]

        theta_rad = math.atan2(y2 - y1, x2 - x1)

        return theta_rad

    def rotation_matrix(self, angle):
        # Computing the rotation matrix
        rotation_mat = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        return rotation_mat
    
    def rotate(self, angle):
        # 2D rotation matrix
        rotation_matrix = self.rotation_matrix(angle)
        
        # Position vector
        position_vector = np.array([[self.robot_pose['x']], [self.robot_pose['y']]])

        # Rotating
        rotated_vector = np.dot(rotation_matrix, position_vector)

        # Updating pose
        self.robot_pose['x'] = rotated_vector[0][0]
        self.robot_pose['y'] = rotated_vector[1][0]
        self.robot_pose['theta'] += np.degrees(angle)

    def translate(self, p1, p2):
        # Finding the distance p2-p1
        distance = np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

        # Translation
        self.robot_pose['x'] += distance * np.cos(np.radians(self.robot_pose['theta']))
        self.robot_pose['y'] += distance * np.sin(np.radians(self.robot_pose['theta']))

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

        