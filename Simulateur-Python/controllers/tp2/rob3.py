import numpy as np

class Robot:
    def __init__(self):
        self.pose = {'x': 0.0, 'y': 0.0, 'theta': 0.0}
        self.wheel_radius_cm = 0.5  # in centimeters
        self.track_width_cm = 2.0  # in centimeters

    def rotate_to_point(self, target_point):
        # Calculate rotation angle to face the target point
        delta_x = target_point['x'] - self.pose['x']
        delta_y = target_point['y'] - self.pose['y']
        target_theta = np.arctan2(delta_y, delta_x)
        rotation_angle = target_theta - self.pose['theta']

        # Perform rotation
        self.rotate(rotation_angle)

    def translate_to_point(self, target_point):
        # Calculate translation distance to reach the target point
        delta_x = target_point['x'] - self.pose['x']
        delta_y = target_point['y'] - self.pose['y']
        translation_distance = np.sqrt(delta_x**2 + delta_y**2)

        # Perform translation
        self.translate(translation_distance)

    def rotate(self, angle_rad):
        # Perform rotation
        # Update robot pose based on the rotation
        self.pose['theta'] += angle_rad

    def translate(self, distance_cm):
        # Perform translation
        # Update robot pose based on the translation
        self.pose['x'] += distance_cm * np.cos(self.pose['theta'])
        self.pose['y'] += distance_cm * np.sin(self.pose['theta'])

    def follow_trajectory(self, trajectory):
        for target_point in trajectory:
            self.rotate_to_point(target_point)
            self.translate_to_point(target_point)


# Example usage
robot = Robot()

# Define a trajectory with multiple waypoints
labyrinth_trajectory = [
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

print("Initial Pose:", robot.pose)

# Follow the trajectory
robot.follow_trajectory(labyrinth_trajectory)

# Display the final pose
print("Final Pose:", robot.pose)

