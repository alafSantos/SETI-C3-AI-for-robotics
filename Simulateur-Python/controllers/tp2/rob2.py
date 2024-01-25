# from graph_walls import graphWalls
# from kinematics_func import kinematicsFunctions # a class I wrote


# k = kinematicsFunctions()

# w = graphWalls()

# # Example robot path
# walls = w.build_the_walls()


# positionC = []
# positionS = []

# positionC.append({'x': -0.5, 'y': 0.125, 'theta': 0.0})
# positionS.append([0.12500000001326772, -1.756502555320949e-05, -0.5000001902857907])

# positionC.append({'x': -0.5, 'y': 0.125, 'theta': 0.0})
# positionS.append([0.1250000000128976, -2.006781947059416e-05, -0.5000002039309354])

# positionC.append({'x': -0.5, 'y': 0.125, 'theta': 0.0})
# positionS.append([0.12500000001289763, -2.006781947117703e-05, -0.5000002039309229])

# positionC.append({'x': -0.5, 'y': 0.125, 'theta': 0.0})
# positionS.append([0.12500000001289763, -2.006781947117703e-05, -0.5000002039309229])

# positionC.append({'x': -0.5, 'y': 0.125, 'theta': 0.0})
# positionS.append([0.12500000001289763, -2.006781947117703e-05, -0.5000002039309229])

# positionC.append({'x': -0.5, 'y': 0.125, 'theta': 0.0})
# positionS.append([0.12500000001289763, -2.006781947117703e-05, -0.5000002039309229])

# positionC.append({'x': -0.3970999999999992, 'y': 0.125, 'theta': 0.0})
# positionS.append([0.12500000187496843, -2.006584664463601e-05, -0.3977245958668025])

# positionC.append({'x': -0.2920999999999983, 'y': 0.125, 'theta': 0.0})
# positionS.append([0.12500000277894133, -2.006584651452481e-05, -0.2927259538314858])

# positionC.append({'x': -0.18709999999999832, 'y': 0.125, 'theta': 0.0})
# positionS.append([0.12500000230078684, -2.0065846713483715e-05, -0.18772731179614324])

# positionC.append({'x': -0.18289999999999826, 'y': 0.125, 'theta': 0.0})
# positionS.append([0.12500000248017779, -2.0067819510770357e-05, -0.18336089235544703])


# def rotate_points(objects):
#     rotated_objects = []
#     for obj in objects:
#         x = obj['x']
#         y = obj['y']

#         # Apply 90 degrees rotation
#         x_rotated = -y
#         y_rotated = x

#         rotated_object = {'x': x_rotated, 'y': y_rotated, 'theta': obj['theta']}
#         rotated_objects.append(rotated_object)

#     return rotated_objects

# positionC = rotate_points(positionC)

# for p in positionC:
#     w.plot_robot(100*p["x"], 100*p["y"], walls)

# def dot_product(x, y):
#     dp = 0
#     for i in range(len(x)):
#         dp += (x[i]*y[i])
#     return dp

# p1 = [-0.5, 0.125]
# p2 = [-0.1, 0.1]

# R = k.rotation_matrix(p1, p2)

# pl = R*p2
# O = k.translation_vector(p1, p2)
# pd = pl + O

# print("Starting Point:", p1)
# print("Destination Point:", p2)
# print("Rotation Matrix:")
# print(R)
# print("Translation Vector:")
# print(O)
# print("Final Point after Rotation and Translation:")
# print(dot_product(R, p1))



# Starting point
# x1, y1 = 0.000001, 0.000001 #-0.5, 0.125

# # Destination point
# x2, y2 = -0.1, 0.1

# # Find rotation matrix and translation vector
# rot_mat = rotation_matrix(x1, y1, x2, y2)
# trans_vec = translation_vector(x1, y1, x2, y2)

# # Apply rotation and translation to starting point
# starting_point = np.array([x1, y1, 1])  # Homogeneous coordinates
# rotation_translation_matrix = np.column_stack([np.row_stack([rot_mat, [0, 0]]), [trans_vec[0], trans_vec[1], 1]])
# final_point_homogeneous = np.dot(rotation_translation_matrix, starting_point)

# # Normalize by the third coordinate
# final_point = final_point_homogeneous[:2] / final_point_homogeneous[2]


from kinematics_func import kinematicsFunctions

if __name__ == "__main__":
    p1 = [-0.5, 0.125]
    p2 = [-0.1, 0.1]

    k = kinematicsFunctions(-0.5, 0.125, 0)
    print("Destination: ", p2)

    print("Initial pose: ", k.get_pose())

    angle_to_destination = k.angle_between_vectors(p1, p2)

    k.rotate(angle_to_destination)

    k.translate(p1, p2)
    
    print("Final pose: ", k.get_pose())