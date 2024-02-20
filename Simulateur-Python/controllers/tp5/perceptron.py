import numpy as np
import matplotlib.pyplot as plt
from flags_file import flags

# Define variables x1 and x2 with values 0 and/or 1.
x1 = [0, 0, 1, 1]
x2 = [0, 1, 0, 1]

# Function to calculate s
def get_s(x, w):
    s = np.dot(x,w)
    return s

# Function to calculate y
def get_y(s):
    return s > 0

# Function to test OR gate and find weights
def test_gate(X1, X2, W):
    for i, xi in enumerate(X1):
        s = get_s([1, X1[i], X2[i]], W)
        y = get_y(s)
        print("x = ", X1[i], X2[i], "y = ", y)

def inference(X,W):
    s=np.dot(X,W)
    y=s>0
    return y

def f_analogique(x):
    y = x
    
    if x < -1:
        y = -1
    elif x > 1:
        y = 1

    return y


def find_weights(gate):
    # Iterate through each x value one at a time to find weights
    for w0 in [i * 0.1 for i in range(-10, 11)]: # from -1 up to 1, step = 0.1
        for w1 in [i * 0.1 for i in range(-10, 11)]:
            for w2 in [i * 0.1 for i in range(-10, 11)]:
                all_correct = True
                for i in range(len(x1)):
                    s = get_s([1,x1[i],x2[i]],[w0,w1,w2])
                    y = get_y(s)
                    if gate == "OR":
                        if not (y == (x1[i] or x2[i])):  # Check if output matches OR gate truth table
                            all_correct = False
                            break
                    if gate == "AND":
                        if not (y == (x1[i] and x2[i])):  # Check if output matches AND gate truth table
                            all_correct = False
                            break
                    elif gate == "XOR":
                        if not (y == (x1[i] ^ x2[i])):  # Check if output matches XOR gate truth table
                            all_correct = False
                            break
                if all_correct:
                    print("Found weights for", gate, "gate:", "w0 =", w0, ", w1 =", w1, ", w2 =", w2)
                    test_gate(x1, x2, [w0, w1, w2])
                    break
            if all_correct:
                break
        if all_correct:
            break

def plot_input_plan_weight(x1, x2, t):
    x = [0, t]
    y = [t, 0]

    plt.plot(x, y, 'r')
    
    xpoints = np.array(x1)
    ypoints = np.array(x2)

    plt.plot(xpoints, ypoints, 'o')
    plt.xlabel("x1")
    plt.ylabel("x2")
    plt.grid()

    plt.show()    

if flags["debug"]:
    print("-------------------------------------------------------------------")
    find_weights("OR")
    print("-------------------------------------------------------------------")
    find_weights("AND")
    print("-------------------------------------------------------------------")
    find_weights("XOR") # https://humphryscomputing.com/Notes/Neural/single.neural.html

    print("-------------------------------------------------------------------")
    plot_input_plan_weight(x1, x2, 0.5) # OR
    test_gate(x1, x2, [0.0, 1.0, 1.0])
    
    print("-------------------------------------------------------------------")
    plot_input_plan_weight(x1, x2, 1) # AND
    test_gate(x1, x2, [-1.5, 1.0, 1.0])
    