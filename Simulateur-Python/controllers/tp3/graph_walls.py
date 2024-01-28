'''
Developed by Alaf DO NASCIMENTO SANTOS in the context of the Artificial Intelligence for Robotics course. Master SETI.

graphWalls class - This class helps in displaying the simulated robot in a 2D view using the matplotlib library
'''

import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class graphWalls():
    def __init__(self):
        # Initialise the figure
        self.fig, self.ax = plt.subplots()

        # Define axis limits
        self.lim = 100

    def build_the_walls(self):
        # Wall coordinates
        walls = [
            {'x': [-0.25, 0.25, 0.25, 0.75, 0.75], 'y': [-0.75, -0.75, 0.25, 0.25, 0.75]}, # external shape pt1
            {'x': [0.75, -0.25, -0.25, -0.75, -0.75, -0.25, -0.25], 'y': [0.75, 0.75, 0.25, 0.25, -0.25, -0.25, -0.75]}, # external shape pt2
            {'x': [0.5, 0, 0], 'y': [0.5, 0.5, -0.5]}, # center pt1
            {'x': [-0.5, 0], 'y': [0, 0]}, # center pt2
        ]

        # Rotating for better user visualisation
        for wall in walls:
            rotated_x = [round(math.cos(math.radians(90)) * x - math.sin(math.radians(90)) * y, 2) for x, y in zip(wall['x'], wall['y'])]
            rotated_y = [round(math.sin(math.radians(90)) * x + math.cos(math.radians(90)) * y, 2) for x, y in zip(wall['x'], wall['y'])]
            wall['x'] = rotated_x
            wall['y'] = rotated_y

        # Increasing scale for better user visualisation
        factor = 100

        for wall in walls:
            wall['x'] = [x * factor for x in wall['x']]
            wall['y'] = [y * factor for y in wall['y']]
            
        return walls
    
    def plot_robot(self, x, y, color='blue', destination=False):
        # Getting the pre-processed walls
        walls = self.build_the_walls()

        # Set aspect ratio to equal
        self.ax.set_aspect('equal', 'box')

        # Set labels and title
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.set_title('Robot walking through the labyrinth')

        # Create animation
        plt.ion()
        if destination:
            self.ax.plot(x, y, '+', color=color)
        else:
            self.ax.plot(x, y, '*', color=color)

        # Plot the walls
        for wall_line in walls:
            self.ax.add_line(Line2D(wall_line['x'], wall_line['y'], color='gray'))
        self.ax.set_xlim([-self.lim, self.lim])
        self.ax.set_ylim([-self.lim, self.lim])

        plt.draw()
        plt.pause(0.001)

