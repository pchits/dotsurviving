import numpy as np
import csv

# with this article's help https://school.geekwall.in/p/Sy9NonT37/creating-a-neural-network-from-scratch-in-python

class NeuralNetwork:
    def __init__(self, x, y):
        self.input = x
        self.weights1 = np.random.rand(self.input.shape[1],4)
        self.weights2 = np.random.rand(4,1)
        self.y = y
        self.output = np.zeros(self.y.shape)

    def sigmoid(self, x):
        return 1.0/(1+ np.exp(-x))

    def sigmoid_derivative(self, x):
        return x * (1.0 - x)

    def feedforward(self):
        self.layer1 = self.sigmoid(np.dot(self.input, self.weights1))
        self.output = self.sigmoid(np.dot(self.layer1, self.weights2))

    def backprop(self):
        # application of the chain rule to find derivative of the loss function with respect to weights2 and weights1
        d_weights2 = np.dot(self.layer1.T, (2*(self.y - self.output) * self.sigmoid_derivative(self.output)))
        d_weights1 = np.dot(self.input.T,  (np.dot(2*(self.y - self.output) * self.sigmoid_derivative(self.output), self.weights2.T) * self.sigmoid_derivative(self.layer1)))

        # update the weights with the derivative (slope) of the loss function
        self.weights1 += d_weights1
        self.weights2 += d_weights2

    def load(self):
        self.weights1 = self.read_weight('1')
        self.weights2 = self.read_weight('2')
        
    def save(self):
        self.write_weight('1', self.weights1)
        self.write_weight('2', self.weights2)

    def read_weight(self, w_name):
        W = []
        with open('weight' + w_name + '.csv', mode = 'r') as csv_file:
            data = list(csv.reader(csv_file))
        for line in data:
            line_write = []
            for w in line:
                line_write.append(float(w))
            W.append(line_write)
        W = np.array(W)
        return W

    def write_weight(self, w_name, data):
        with open('weight' + w_name + '.csv', 'w', newline = '') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)