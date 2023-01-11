# -*- coding: utf-8 -*-
"""mini_project3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1boSBlNegTn4UfVXqTdIMJZQuwfjp32G4

# Mini Project 3
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
# %matplotlib notebook
# %matplotlib inline
import matplotlib.pyplot as plt
import tensorflow as tf

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D

"""## Task 1: Acquire the data

load dataset using tensorflow library
"""

(X_train, y_train), (X_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()
X_train.shape
print(len(X_train))

"""We start by transforming the training and test sets into a 1D array. 


"""

y_train_arr = []
for i in range(len(y_train)):
  y_train_zeros = np.zeros(9)
  a = np.insert(y_train_zeros, y_train[i], 1)
  y_train_arr.append(a)

X_train = np.copy(X_train)
X_train_f = X_train.astype(np.float64)
X_train_f -= np.mean(X_train_f)
X_train_f /= np.std(X_train_f)

X_test = np.copy(X_test)
X_test_f = X_test.astype(np.float64)
X_test_f -= np.mean(X_test_f)
X_test_f /= np.std(X_test_f)

X_train_vect = X_train.reshape(X_train_f.shape[0], (X_train_f.shape[1]*X_train_f.shape[2]))
X_test_vect = X_test.reshape(X_test_f.shape[0], (X_test_f.shape[1]*X_test_f.shape[2]))
from matplotlib import pyplot
pyplot.imshow(X_train[0])

"""## Task 2: Implement a Multilayer Perceptron

Multilayer Perceptron Class (to be finished)
"""

#define activation functions and their derivatives
def relu(x):
  return 0.0 if x < 0.0 else x
relu_v = np.vectorize(relu)
def relu_deriv(x):
  return 0.0 if x < 0.0 else 1.0
relu_deriv_v = np.vectorize(relu_deriv)
def leaky_relu(x):
  return 0.1 * x if x < 0 else x
leaky_relu_v = np.vectorize(leaky_relu)
def leaky_deriv(x):
  return 0.1 if x < 0 else 1
leaky_deriv_v = np.vectorize(leaky_deriv)
def tanh(x):
  return np.tanh(x)
tanh_v = np.vectorize(tanh)
def tanh_deriv(x):
  return 0.1 - np.tanh(x)**2
tanh_deriv_v = np.vectorize(tanh_deriv)

def softmax(x):
  e_x = np.exp(x - np.max(x))
  return e_x / e_x.sum(axis=0)

def cross_entropy(yh, y):
    if y == 1.0:
      return -np.log(yh)
    else:
      return -np.log(1 - yh)

def log_softmax(x):
    c = x.max()
    logsumexp = np.log(np.exp(x - c).sum())
    return x - c - logsumexp


class MultilayerPerceptron:
    
    def __init__(self, activation_function, activation_derivative, num_hidden_layers, num_units_hidden_layers):
      self.activation_function = activation_function
      self.activation_derivative = activation_derivative
      self.num_hidden_layers = num_hidden_layers
      self.num_units_hidden_layers = num_units_hidden_layers
      D = [28,28]
      C = 9
      # initialize weights and bias' randomly
      hidden_layers = []
      for i in range(num_hidden_layers):
        hidden_layers.append(num_units_hidden_layers)
      
      layers = [2] + hidden_layers + [1]

      weights = []
      bias = []
      for i in range(len(layers) - 1):
        w = np.random.randn(layers[i], layers[i + 1]) * 0.01
        weights.append(w)
        b = np.full(layers[i + 1], 0.1)
        bias.append(b)
      self.weights = weights
      self.bias = bias


      activations = []
      for i in range(len(layers)):
        a = np.zeros(layers[i])
        activations.append(a)
      self.activations = activations

      derivatives = [] 
      for i in range(len(layers) - 1):
        d = np.zeros((layers[i], layers[i+1]))
        derivatives.append(d)
      self.derivatives = derivatives

    def forward_propagate(self, inputs):
      activations = inputs
      self.activations[0] = inputs

      for i, w in enumerate(self.weights):
        b = self.bias[i]
        
        net_inputs = np.dot(activations, w) 

        # print(net_inputs)

        # apply activation function
        activations = self.activation_function(net_inputs)
        # if(i == len(self.weights) - 1):
        #   activations = softmax(activations)

        # print(activations)
        self.activations[i+1] = activations

      return activations

    def back_propagate(self, error):
      for i in reversed(range(len(self.derivatives))):
        activations = self.activations[i+1]
        delta = error * self.activation_derivative(activations) 
        delta_reshaped = delta.reshape(delta.shape[0], -1).T     #1D array to 2D array with single row
        current_activations = self.activations[i] 
        current_activations_reshaped = current_activations.reshape(current_activations.shape[0], -1) #1D array to 2D array with multiple rows

        self.derivatives[i] = np.dot(current_activations_reshaped, delta_reshaped)
        error = np.dot(delta, self.weights[i].T)
      


    # need to add bias
    def gradient_descent(self, learning_rate):
      for i in range(len(self.weights)):
        weigths = self.weights[i]
        derivatives = self.derivatives[i]
        weigths += derivatives * learning_rate

    def fit(self, inputs, targets, learning_rate, num_of_iterations):

      for i in range(num_of_iterations):
        # iterate through every input and its target one by one
        for x, y in zip(inputs, targets):
          #forward propagate
          output = self.forward_propagate(x)

          #calculate error
          # error = 0
          # for i in range(len(output)):
          #   output[i] = max(1e-9, output[i])

          # error = -np.sum(y * np.log(output))
          # error = np.log(error)
          # for i in range(len(y)):
          #   val = cross_entropy(output[i], y[i])
          #   error += val

          error = y - output

          #back propagate
          self.back_propagate(error)

          self.gradient_descent(learning_rate)
      
    def predict(self, inputs):
      # predictions = []
      for x in inputs:
        prediction = self.forward_propagate(x)    
        print(prediction)
      #   predictions.append(prediction)
      # return predictions

    def evaluate_acc(self, true_targets, predicted_targets):
      errors = []
      for true, pred in zip(true_targets, predicted_targets):
        error = true - pred
        errors.append(error)
      
      accuracy = np.mean(errors)
      return accuracy

#test 
mlp = MultilayerPerceptron(relu_v, relu_deriv_v, 2, 128)

mlp.fit(X_train_vect[0:8], y_train_arr[0:8], 0.01, 5)

print(relu_v(-5))

# predictions do not work and give NAN 
output = mlp.forward_propagate(X_test_vect[0])
print(output)
print(y_test[0])



from random import random
items = np.array([[random()/2 for _ in range(2)] for _ in range(1000)])
targets = np.array([[i[0] + i[1]] for i in items])

mlp2 = MultilayerPerceptron(relu_v, relu_deriv_v, 2, 5)

mlp2.fit(items, targets, 0.01, 50)

# create dummy data
inputss = np.array([0.3, 0.1])
target = np.array([0.4])

# get a prediction
output = mlp2.forward_propagate(inputss)

print()
print("Our network believes that {} + {} is equal to {}".format(inputss[0], inputss[1], output[0]))

model = Sequential()
 model.add(Conv2D(32, (5, 5), input_shape=(28, 28, 1),    
  activation='relu'))
 model.add(MaxPooling2D())
 model.add(Dropout(0.2))
 model.add(Flatten())
 model.add(Dense(1, activation='relu'))
 model.add(Dense(1, activation='softmax'))

 model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200)

model = Sequential()

model.add(Conv2D(32, (3, 3), padding="Same", activation="relu", input_shape=[28, 28, 1]))
#model.add(MaxPooling2D())
#model.add(Dropout(0.2))

model.add(Conv2D(64, (3, 3), padding="Same", activation="relu"))
#model.add(MaxPooling2D())
#model.add(Dropout(0.2))

model.add(Flatten())
model.add(Dense(128, activation='relu'))
#model.add(Dropout(0.5))
model.add(Dense(128, activation='relu'))

model.compile(loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200)