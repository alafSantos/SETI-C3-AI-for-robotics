import numpy as np
import matplotlib.pyplot as plt

def get_discretised_walls(walls):
        discretized_walls_x = []
        discretized_walls_y = []

        for wall in walls:
            # print("hey ", wall)
            wall_x = []
            wall_y = []
            for i in range(len(wall['x']) - 1):
                x0, y0 = wall['x'][i], wall['y'][i]
                x1, y1 = wall['x'][i + 1], wall['y'][i + 1]
                length = np.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)
                
                num_steps = int(length * 100)  # converting length to cm

                x_step = (x1 - x0) / (num_steps + 1e-100)
                y_step = (y1 - y0) / (num_steps + 1e-100)

                for j in range(num_steps):
                    x_aux = round((x0 + j * x_step)*100)
                    y_aux = round((y0 + j * y_step)*100)

                    wall_x.append(x_aux)
                    wall_y.append(-y_aux)

            discretized_walls_x.append(wall_y)
            discretized_walls_y.append(wall_x)

        return discretized_walls_x[0], discretized_walls_y[0]
        

walls_ext = [
            {'x': [-0.25, 0.25, 0.25, 0.75, 0.75], 'y': [-0.75, -0.75, 0.25, 0.25, 0.75]}, # external shape pt1
        ]

walls_ext2 = [
     {'x': [0.75, -0.25, -0.25, -0.75, -0.75, -0.25, -0.25], 'y': [0.75, 0.75, 0.25, 0.25, -0.25, -0.25, -0.75]} # external shape pt2
    ]

walls_int = [
     {'x': [0.5, 0, 0], 'y': [0.5, 0.5, -0.5]} # center pt1
]

walls_int2 = [
    {'x': [-0.5, 0], 'y': [0, 0]} # center pt2
]

# x_list_int, y_list_int = get_discretised_walls(walls_int)

# x_list_int2, y_list_int2 = get_discretised_walls(walls_int2)

# x_list_ext, y_list_ext = get_discretised_walls(walls_ext)

# x_list_ext2, y_list_ext2 = get_discretised_walls(walls_ext2)


# print(x_list_int)
# print(x_list_int2)
# print("-"*75)
# print(x_list_ext)
# print(x_list_ext2)
# print("-"*75)
# print("-"*75)
# print(y_list_int)
# print(y_list_int2)
# print("-"*75)
# print(y_list_ext)
# print(y_list_ext2)


# plt.plot(x_list_ext, y_list_ext, '+', color='red')
# plt.plot(x_list_int, y_list_int, '+', color='blue')
# plt.plot(x_list_ext2, y_list_ext2, '+', color='black')
# plt.plot(x_list_int2, y_list_int2, '+', color='green')
# plt.show()


# Wall coordinates
walls = [
    {'x': [-0.25, 0.25, 0.25, 0.75, 0.75, 0.75, -0.25, -0.25, -0.75, -0.75, -0.25, -0.25], 'y': [-0.75, -0.75, 0.25, 0.25, 0.75, 0.75, 0.75, 0.25, 0.25, -0.25, -0.25, -0.75]}, # external shape
]

walls_int = [
     {'x': [0.5, 0, 0], 'y': [0.5, 0.5, -0.5]} # center pt1
]

walls_int2 = [ 
    {'x': [-0.5, 0], 'y': [0, 0]}, # center pt2
]

x_list, y_list = get_discretised_walls(walls)
x_list_int, y_list_int = get_discretised_walls(walls_int)
x_list_int2, y_list_int2 = get_discretised_walls(walls_int2)

plt.plot(x_list, y_list, '.', color='blue')
plt.plot(x_list_int, y_list_int, '.', color='blue')
plt.plot(x_list_int2, y_list_int2, '.', color='blue')
plt.xlim(-100, 100)
plt.ylim(-100, 100)
plt.axis("equal")
plt.grid()
plt.show()