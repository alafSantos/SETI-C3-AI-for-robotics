import numpy as np
import matplotlib.pyplot as plt
from flags_file import flags

x_range = [-2.0, 2.0]
w_range = [-1.0, 1.0]

def f_activation_sat(x, w):
    s_vec = np.dot(x,w)
    y_vec = []
    for s in s_vec:
        if s < -1:
            y = -1
        elif s > 1:
            y = 1
        else:
            y = float(s[0])
        y_vec.append(y)

    return y_vec

def plot_y(x, y, titre):
    plt.plot(x, np.reshape(y,21))
    plt.grid()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(titre)
    plt.show()

# Exercice 1
if flags["exercice_1"]:
    step = .2
    x1 = np.arange(x_range[0], x_range[1] + step, step)
    w1 = [-0.5]

    y1 = f_activation_sat(np.matrix(x1).T, np.matrix(w1))

    plt.plot(x1, np.reshape(y1,21))
    plt.grid()
    plt.xlabel('x1')
    plt.ylabel('y1')
    titre = "x1 par rapport à y1 (avec w1 = " + str(w1[0]) + ")"
    plt.title(titre)
    plt.show()

# Exercice 2
if flags["exercice_2"]:
    for i in range(15):
        w1_val = -1.0 + i * (2.0 / 14)  # Adjust to get 15 values in the range [-1, 1]
        w1 = [w1_val]
        y1 = f_activation_sat(np.matrix(x1).T, np.matrix(w1))
        plt.plot(x1, np.reshape(y1,21), label=f'w1 = {w1_val}')

    plt.grid()
    plt.xlabel('x1')
    plt.ylabel('y1')
    plt.title('x1 en fonction de y1 pour différentes valeurs de w1')
    plt.legend()
    plt.show()

# Exercice 3 (EM DESENVOLVIMENTO)
if flags["exercice_3"]:
    w11 = 1.0
    w12 = 0.5
    w21 = 1.0
    w22 = -1.0

    w1 = [w11]
    w2 = [w12]
    w3 = [w21, w22]

    y1 = f_activation_sat(np.matrix(x1).T, np.matrix(w1))
    y2 = f_activation_sat(np.matrix(x1).T, np.matrix(w2))

    y3 = f_activation_sat(np.matrix([y1,y2]).T, np.matrix(w3).T)

    plot_y(x1, y3, "ex 3")

# Exercice 4 - dans webots
