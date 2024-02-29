import numpy as np
import matplotlib.pyplot as plt

x_range = [-2.0, 2.0]
w_range = [-1.0, 1.0]

# Exercice 1
def f_activation_sat(x, w):
    s_vec = x*np.transpose(w)
    y_vec = []
    for s in s_vec:
        if s < -1:
            y = -1
        elif s > 1:
            y = 1
        else:
            y = s
        y_vec.append(y)

    return y_vec

step = .2
x1 = np.arange(x_range[0], x_range[1] + step, step)
w1 = [-0.5]*len(x1)
print(x1)

y1 = f_activation_sat(x1, w1)

plt.plot(y1, x1)
plt.grid()
plt.xlabel('y1')
plt.ylabel('x1')
titre = "x1 par rapport à y1 (avec w1 = " + str(w1[0]) + ")"
plt.title(titre)
plt.show()

# Exercice 2
for i in range(15):
    w1_val = -1.0 + i * (2.0 / 14)  # Adjust to get 15 values in the range [-1, 1]
    w1 = [w1_val] * len(x1)
    y1 = f_activation_sat(x1, w1)
    plt.plot(y1, x1, label=f'w1 = {w1_val}')

plt.grid()
plt.xlabel('y1')
plt.ylabel('x1')
plt.title('x1 en fonction de y1 pour différentes valeurs de w1')
plt.legend()
plt.show()

# Exercice 3 (EM DESENVOLVIMENTO)
w11 = 1.0
w12 = 0.5
w21 = 1.0
w22 = -1.0
w = [[w11, w12], [w21, w22]]
