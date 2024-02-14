# Define variables x1 and x2 with values 0 and/or 1.
x1 = [0, 0, 1, 1]
x2 = [0, 1, 0, 1]

# Function to calculate s
def get_s(x1, x2, w0, w1, w2):
    s = w0 + w1*x1 + w2*x2
    return s

# Function to calculate y
def get_y(s):
    y = 1
    if s < 0:
        y = 0
    return y

# Function to test OR gate and find weights
def test_gate(x1, x2, w0, w1, w2):
    for i in range(len(x1)):
        s = get_s(x1[i], x2[i], w0, w1, w2)  # Using unknown weights w0, w1, w2
        y = get_y(s)
        print("x1 =", x1[i], ", x2 =", x2[i], ", s =", s, ", y =", y)

def find_weights(gate):
    # Iterate through each x value one at a time to find weights
    for w0 in [i * 0.1 for i in range(-10, 11)]: # from -1 up to 1, step = 0.1
        for w1 in [i * 0.1 for i in range(-10, 11)]:
            for w2 in [i * 0.1 for i in range(-10, 11)]:
                all_correct = True
                for i in range(len(x1)):
                    s = get_s(x1[i], x2[i], w0, w1, w2)
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
                    test_gate(x1, x2, w0, w1, w2)
                    break
            if all_correct:
                break
        if all_correct:
            break

print("-------------------------------------------------------------------")
find_weights("OR")
print("-------------------------------------------------------------------")
find_weights("AND")
print("-------------------------------------------------------------------")
find_weights("XOR") # https://humphryscomputing.com/Notes/Neural/single.neural.html