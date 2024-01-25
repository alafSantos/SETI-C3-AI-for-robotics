import numpy as np
import math

class kinematicsFunctions():
    def __init__(self, x=-0.5, y=0.125, orientation=0):
        # Initial Pose
        self.robot_pose = {'x': x, 'y': y, 'theta': orientation}

        # Physical information of the robot
        self.wheel_radius = 2.1 * 1e-2
        self.track_width = 10.8 * 1e-2
        
        # Trajectory variable
        self.path = {'x': [], 'y': []}

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
        linear_displacement = (left_wheel_displacement + right_wheel_displacement) / 2

        # Calculate rotational displacement
        angular_displacement = (left_wheel_displacement - right_wheel_displacement) / self.track_width
        
        return linear_displacement, angular_displacement
    

    def get_pose(self):
        return self.robot_pose

    def get_new_pose(self, left_wheel_speed, right_wheel_speed, dt):
        # Calculate linear and angular displacements
        linear_displacement, angular_displacement = self.get_displacements(left_wheel_speed, right_wheel_speed, dt)

        # Update robot pose based on wheel speeds
        delta_theta = angular_displacement * dt

        self.robot_pose['x'] += linear_displacement * np.cos(self.robot_pose['theta'] + delta_theta/2)
        self.robot_pose['y'] += linear_displacement * np.sin(self.robot_pose['theta'] + delta_theta/2)
        self.robot_pose['theta'] += delta_theta

        # Update traveled path
        self.path['x'].append(self.robot_pose['x'])
        self.path['y'].append(self.robot_pose['y'])

        return self.robot_pose
    
    def get_path(self):
        return self.path   

    def angle_between_vectors(self, p1, p2):
        # Separete the values
        x1, y1 = p1[0], p1[1]
        x2, y2 = p2[0], p2[1]

        # dot_product = x1 * x2 + y1 * y2
        # magnitude_v1 = np.sqrt(x1**2 + y1**2)
        # magnitude_v2 = np.sqrt(x2**2 + y2**2)
        # cosine_theta = dot_product / (magnitude_v1 * magnitude_v2)
        # theta_rad = np.arccos(cosine_theta)

        theta_rad = math.atan2(y2 - y1, x2 - x1)

        return theta_rad

    def rotation_matrix(self, angle):
        rotation_mat = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        return rotation_mat
    
    def rotate(self, angle):
        # 2D rotation matrix
        rotation_matrix = self.rotation_matrix(angle)
        print("Rotation matrix: \n", rotation_matrix)
        
        # Position vector
        position_vector = np.array([[self.robot_pose['x']], [self.robot_pose['y']]])

        # Rotating
        rotated_vector = np.dot(rotation_matrix, position_vector)

        # Updating pose
        self.robot_pose['x'] = rotated_vector[0][0]
        self.robot_pose['y'] = rotated_vector[1][0]
        self.robot_pose['theta'] += math.degrees(angle)

    def translate(self, p1, p2):
        # Finding the distance p2-p1
        distance = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

        # Translation
        self.robot_pose['x'] += distance * math.cos(math.radians(self.robot_pose['theta']))
        self.robot_pose['y'] += distance * math.sin(math.radians(self.robot_pose['theta']))

        