import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class graphWalls():
    def __init__(self):
        self.walls = []
        self.x0 = 0
        self.y0 = 0

        self.fig, self.ax = plt.subplots()

        # Set axis limits
        lim = 100
        self.ax.set_xlim([-lim, lim])
        self.ax.set_ylim([-lim, lim])

    def build_the_walls(self):
        walls = [
            {'x': [-0.25, 0.25, 0.25, 0.75, 0.75], 'y': [-0.75, -0.75, 0.25, 0.25, 0.75]}, # external shape pt1
            {'x': [0.75, -0.25, -0.25, -0.75, -0.75, -0.25, -0.25], 'y': [0.75, 0.75, 0.25, 0.25, -0.25, -0.25, -0.75]}, # external shape pt2
            {'x': [0.5, 0, 0], 'y': [0.5, 0.5, -0.5]}, # center pt1
            {'x': [-0.5, 0], 'y': [0, 0]}, # center pt2
        ]

        for wall in walls:
            rotated_x = [round(math.cos(math.radians(90)) * x - math.sin(math.radians(90)) * y, 2) for x, y in zip(wall['x'], wall['y'])]
            rotated_y = [round(math.sin(math.radians(90)) * x + math.cos(math.radians(90)) * y, 2) for x, y in zip(wall['x'], wall['y'])]
            wall['x'] = rotated_x
            wall['y'] = rotated_y

        factor = 100

        for wall in walls:
            wall['x'] = [x * factor for x in wall['x']]
            wall['y'] = [y * factor for y in wall['y']]
        
        self.walls = walls

        return self.walls
    
    def plot_robot(self, x, y, wall_lines):
        # Plot the walls
        for wall_line in wall_lines:
            self.ax.add_line(Line2D(wall_line['x'], wall_line['y'], color='gray'))

        # Set aspect ratio to equal
        self.ax.set_aspect('equal', 'box')

        # Set labels and title
        self.ax.set_xlabel('X-axis')
        self.ax.set_ylabel('Y-axis')
        self.ax.set_title('Robot Walking Through the Path')

        # Display the plot
        plt.grid(True)

        # Create animation
        # tmp, = ax.plot(self.x0, self.y0, 'bo')
        plt.ion()
        tmp, = self.ax.plot(x, y, 'bo')
        plt.draw()
        plt.pause(0.4)
        # plt.clf()

        # label = "(x, y) = " + "(" + str(x) + ", " + str(y) + ")"
        # tmp.remove()
        # self.x0 = x
        # self.y0 = y
        # plt.legend()
        # plt.show()
