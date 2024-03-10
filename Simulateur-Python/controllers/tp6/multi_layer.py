import numpy as np
import matplotlib.pyplot as plt
from flags_file import flags

def f_activation_sat_q5(x, w):
    s_vec = np.dot(x,w)
    y_vec = []
    for s in s_vec:
        if s < 0:
            y = 0
        elif s > 1:
            y = 1
        else:
            y = float(s[0])
        y_vec.append(y)

    return y_vec

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

def plot_y(x, y, lx, ly, titre, plot=True):
    if plot:
        plt.plot(x, np.reshape(y,21))
    plt.grid()
    plt.xlabel(lx)
    plt.ylabel(ly)
    plt.title(titre)
    if not plot:
        plt.legend()
    plt.show()

step = .2
x1 = np.arange(-2.0, 2.0 + step, step)

if flags["exercice_1"]:
    w1 = [-0.5]
    y1 = f_activation_sat(np.matrix(x1).T, np.matrix(w1))
    titre = "y1 par rapport à x1 (avec w1 = " + str(w1[0]) + ")"
    plot_y(x1, y1, 'x1', 'y1', titre)

if flags["exercice_2"]:
    for i in range(15):
        w1_val = -1.0 + i * (2.0 / 14)  # Adjust to get 15 values in the range [-1, 1]
        w1 = [w1_val]
        y1 = f_activation_sat(np.matrix(x1).T, np.matrix(w1))
        plt.plot(x1, np.reshape(y1,21), label=f'w1 = {w1_val}')

    titre = 'y1 en fonction de x1 pour différentes valeurs de w1'
    plot_y(x1, y1, 'x1', 'y1', titre, False)

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

    plot_y(x1, y1, "x1", "y1", "y1 en fonction de x1 pour le réseau multicouche")
    plot_y(x1, y2, "x1", "y2", "y2 en fonction de x1 pour le réseau multicouche")
    plot_y(x1, y3, "x1", "y3", "y3 en fonction de x1 pour le réseau multicouche")

if flags["exercice_5"]:
    step = .1
    w_rec_v = np.arange(0, 2.0 + step, step)
    nmbr_step=10
    
    w1=0.5
    for w_rec in w_rec_v:
        x_rec=0
        y_v=[]
        for i in range(nmbr_step):
            x1=(i==0)
            y = f_activation_sat_q5(np.matrix([x1,x_rec]), np.matrix([w1,w_rec]).T)
            x_rec=y[0]
            y_v.append(y)

        plt.plot(range(nmbr_step), y_v, label=f'w_rec = {w_rec}')

    titre = 'Evolution de y1 selon t le passage des échantillons, pour différentes valeurs de w_rec'
    plot_y(w_rec, y_v, 't', 'y_1', titre, False)

