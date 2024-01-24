import numpy as np

class kinematicsFunctions():
    def __init__(self):
        # Initial Pose
        self.robot_pose = {'x': -0.5, 'y': 0.125, 'theta': 0}

        # Physical information of the robot
        self.wheel_radius = 2.1 * 1e-2
        self.track_width = 10.8 * 1e-2
        
        # Trajectory variable
        self.path = {'x': [], 'y': []}


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
    

    def get_pose(self, left_wheel_speed, right_wheel_speed, dt):
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
