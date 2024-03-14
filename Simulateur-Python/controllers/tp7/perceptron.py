from sklearn.linear_model import Perceptron
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from flags_file import flags
import h5py
import numpy as np
import pickle

def get_perceptron_data(operator, labels, MLP=False):
    if MLP:
        print("W0: ", operateurXOR.intercepts_)
        print("Weights: ", operator.coefs_)
    else:
        print("W0: ", operator.intercept_)
        print("Weights: ", operator.coef_)
    print("Predictions: ", operator.predict(data))
    print("Score: ", operator.score(data, labels))

#liste d'entrées possibles pour l'opérateur logique
data = [[0,0], [0,1], [1,0], [1,1]]

#labels correspondants selon liste d'entrées
ORlabels = [0, 1, 1, 1]
ANDlabels = [0, 0, 0, 1]
XORlabels = [0, 1, 1, 0]


if flags["exercice_1_2_3"]:
    #Création du perceptron
    operateurOR = Perceptron(max_iter=40, tol=1e-3)
    operateurAND = Perceptron(max_iter=40, tol=1e-3)
    operateurXOR = Perceptron(max_iter=40, tol=1e-3)

    operateurOR.fit(data, ORlabels)
    operateurAND.fit(data, ANDlabels)
    operateurXOR.fit(data, XORlabels)

    print("\n-----------------------------------------------\n\t\t OR operator")
    get_perceptron_data(operateurOR, ORlabels)

    print("\n-----------------------------------------------\n\t\t AND operator")
    get_perceptron_data(operateurAND, ANDlabels)

    print("\n-----------------------------------------------\n\t\t XOR operator")
    get_perceptron_data(operateurXOR, XORlabels)

elif flags["exercice_4_5_6"] :
    operateurXOR =MLPClassifier(hidden_layer_sizes=(2,),activation="tanh",max_iter=10000)
    operateurXOR.fit(data, XORlabels)

    while operateurXOR.score(data, XORlabels) != 1:
        operateurXOR.fit(data, XORlabels)

    print("\n-----------------------------------------------\n\t\t XOR operator\n")
    get_perceptron_data(operateurXOR, XORlabels, MLP=True)

elif flags["exercice_7"]:
    operateurXOR = MLPRegressor(hidden_layer_sizes=3, activation="tanh", solver="lbfgs")
    operateurXOR.fit(data, XORlabels)

    print("\n-----------------------------------------------\n\t\t XOR operator\n")
    get_perceptron_data(operateurXOR, XORlabels, MLP=True)


elif flags["exercice_9"]:

    # Ouverture du fichier anti-horaire
    with h5py.File('datasets/dataset_webots_anti-horaire.hdf5', 'r') as f:
        # Récupération des datasets
        speed_dataset = f['thymio_speed']
        proximeters_dataset = f['thymio_prox']

        # Conversion des datasets en listes
        speed_array_ah = speed_dataset[:]
        proximeters_array_ah = proximeters_dataset[:]
    
    with h5py.File('datasets/dataset_webots_horaire.hdf5', 'r') as f:
        # Récupération des datasets
        speed_dataset = f['thymio_speed']
        proximeters_dataset = f['thymio_prox']

        # Conversion des datasets en listes
        speed_array_h = speed_dataset[:]
        proximeters_array_h = proximeters_dataset[:]
    
    # Concatenation des listes
    thymio_commands = np.concatenate((speed_array_ah, speed_array_h), axis=0)
    thymio_proximeters = np.concatenate((proximeters_array_ah, proximeters_array_h), axis=0)
    
    # Normalisation
    speed_max = 9.53
    thymio_commands = thymio_commands / speed_max

    # Split du dataset
    prox_x_train, prox_x_test, prox_y_train, prox_y_test = train_test_split(thymio_proximeters, thymio_commands)

    # Définition du réseau et entrainement
    controller = MLPRegressor(hidden_layer_sizes=(2,2), activation="tanh", solver="lbfgs")
    controller.fit(prox_x_train, prox_y_train)

    # Affichage des résultats
    print("W0: ", controller.intercepts_)
    print("Weights: ", controller.coefs_)
    print("Score: ", controller.score(prox_x_test, prox_y_test))

    # Pickle the model
    filename = 'ai_controller_model_hyper_prox.model'
    pickle.dump(controller, open(filename, 'wb'))