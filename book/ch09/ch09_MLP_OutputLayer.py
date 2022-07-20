import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

Z1 = np.array([0.99752738, 0.99999774, 1.        ])

W2 = np.array([[0.1,0.4], [0.2,0.5], [0.3,0.6]])
B2 = np.array([0.1, 0.2])

A2 = np.dot(Z1, W2) + B2
Y = sigmoid(A2)
