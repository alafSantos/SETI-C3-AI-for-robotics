from graph_walls import graphWalls

w = graphWalls()

# Example robot path
walls = w.build_the_walls()


positionC = []
positionS = []

positionC.append({'x': -0.5, 'y': 0.125, 'theta': 0.0})
positionS.append([0.12500000001326772, -1.756502555320949e-05, -0.5000001902857907])

positionC.append({'x': -0.5, 'y': 0.125, 'theta': 0.0})
positionS.append([0.1250000000128976, -2.006781947059416e-05, -0.5000002039309354])

positionC.append({'x': -0.5, 'y': 0.125, 'theta': 0.0})
positionS.append([0.12500000001289763, -2.006781947117703e-05, -0.5000002039309229])

positionC.append({'x': -0.5, 'y': 0.125, 'theta': 0.0})
positionS.append([0.12500000001289763, -2.006781947117703e-05, -0.5000002039309229])

positionC.append({'x': -0.5, 'y': 0.125, 'theta': 0.0})
positionS.append([0.12500000001289763, -2.006781947117703e-05, -0.5000002039309229])

positionC.append({'x': -0.5, 'y': 0.125, 'theta': 0.0})
positionS.append([0.12500000001289763, -2.006781947117703e-05, -0.5000002039309229])

positionC.append({'x': -0.3970999999999992, 'y': 0.125, 'theta': 0.0})
positionS.append([0.12500000187496843, -2.006584664463601e-05, -0.3977245958668025])

positionC.append({'x': -0.2920999999999983, 'y': 0.125, 'theta': 0.0})
positionS.append([0.12500000277894133, -2.006584651452481e-05, -0.2927259538314858])

positionC.append({'x': -0.18709999999999832, 'y': 0.125, 'theta': 0.0})
positionS.append([0.12500000230078684, -2.0065846713483715e-05, -0.18772731179614324])

positionC.append({'x': -0.18289999999999826, 'y': 0.125, 'theta': 0.0})
positionS.append([0.12500000248017779, -2.0067819510770357e-05, -0.18336089235544703])


def rotate_points(objects):
    rotated_objects = []
    for obj in objects:
        x = obj['x']
        y = obj['y']

        # Apply 90 degrees rotation
        x_rotated = -y
        y_rotated = x

        rotated_object = {'x': x_rotated, 'y': y_rotated, 'theta': obj['theta']}
        rotated_objects.append(rotated_object)

    return rotated_objects

positionC = rotate_points(positionC)

for p in positionC:
    w.plot_robot(100*p["x"], 100*p["y"], walls)