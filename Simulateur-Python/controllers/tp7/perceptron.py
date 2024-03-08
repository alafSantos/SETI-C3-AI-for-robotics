from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor

#liste d'entrées possibles pour l'opérateur logique
data = [[0,0], [0,1], [1,0], [1,1]]

#labels correspondants selon liste d'entrées
ORlabels = [0, 1, 1, 1]
ANDlabels = [0, 0, 0, 1]
XORlabels = [0, 1, 1, 0]

#Création du perceptron
operateurOR = Perceptron(max_iter=40, tol=1e-3)
operateurAND = Perceptron(max_iter=40, tol=1e-3)
operateurXOR = Perceptron(max_iter=40, tol=1e-3)

operateurOR.fit(data, ORlabels)
operateurAND.fit(data, ANDlabels)
operateurXOR.fit(data, XORlabels)

def get_perceptron_data(operator, labels, MLP=False):
    if MLP:
        print("W0: ", operateurXOR.intercepts_)
        print("Weights: ", operator.coefs_)
    else:
        print("W0: ", operator.intercept_)
        print("Weights: ", operator.coef_)
    print("Prediction: ", operator.predict(data))
    print("Score: ", operator.score(data, labels))


print("\n-----------------------------------------------\n\t\t OR operator\n")
get_perceptron_data(operateurOR, ORlabels)

print("\n-----------------------------------------------\n\t\t AND operator\n")
get_perceptron_data(operateurAND, ANDlabels)

print("\n-----------------------------------------------\n\t\t XOR operator\n")
get_perceptron_data(operateurXOR, XORlabels)


################################################################################################## 
operateurXOR =MLPClassifier(hidden_layer_sizes=(2,),activation="tanh",max_iter=10000)
operateurXOR.fit(data, XORlabels)

print("\n-----------------------------------------------\n\t\t XOR operator\n")
while operateurXOR.score(data, XORlabels) != 1:
    operateurXOR.fit(data, XORlabels)

print("\n-----------------------------------------------\n\t\t XOR operator\n")
get_perceptron_data(operateurXOR, XORlabels, MLP=True)


##################################################################################################
operateurXOR = MLPRegressor(hidden_layer_sizes=3, activation="tanh", solver="lbfgs")
operateurXOR.fit(data, XORlabels)

print("\n-----------------------------------------------\n\t\t XOR operator\n")
get_perceptron_data(operateurXOR, XORlabels, MLP=True)