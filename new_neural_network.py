import numpy as np
import random

epochs = 50

class NeuralNetwork():

    def __init__(self, max_length):
        self.weights = 2 * np.random.random((max_length, 1)) - 1
        self.activation = sigmoid
        self.derivative = sigmoid_der


    def through(self, inputs):
        inputs = inputs.astype(float)
        output = self.activation(np.dot(inputs, self.weights))
        return output

    def train(self, inputs, outputs, epochs):
        for epoch in range(epochs):
            print("EPOCH : {}".format(epoch))
            output = self.through(inputs)
            loss = outputs - output
            adjustments_np = np.dot(inputs.T, loss * self.derivative(output))
            for i in range(len(adjustments_np)):
                total = 0
                for j in range(len(adjustments_np[i])):
                    total += adjustments_np[i][j]
                total = total / len(adjustments_np[i])
                adjustments_np[i] = total
            self.weights = self.weights + adjustments_np
        print(self.weights)

def sigmoid(x):
    x = 1 / (1 + np.exp(-x))
    return x

def sigmoid_der(x):
    return x * (1-x)

def tanh(x):
    return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

def tanh_der(x):
    return 1 - (x)**2

def findMaxLength(ls):
    max_length = 0
    for x in ls:
        if len(x) > max_length:
            max_length = len(x)
    return max_length

def getAlphabet(sp, sn, tp, tn):
    alphabet = []
    for x in sp:
        ls = x[0]
        for num in ls:
            check = False
            for i in range(len(alphabet)):
                if alphabet[i][0] == num:
                    check = True
                    break
            if (check == False):
                alphabet.append([num, len(alphabet)+1])
    for x in sn:
        ls = x[0]
        for num in ls:
            check = False
            for i in range(len(alphabet)):
                if alphabet[i][0] == num:
                    check = True
                    break
            if (check == False):
                alphabet.append([num, len(alphabet)+1])
    for x in tp:
        ls = x[0]
        for num in ls:
            check = False
            for i in range(len(alphabet)):
                if alphabet[i][0] == num:
                    check = True
                    break
            if (check == False):
                alphabet.append([num, len(alphabet)+1])
    for x in tn:
        ls = x[0]
        for num in ls:
            check = False
            for i in range(len(alphabet)):
                if alphabet[i][0] == num:
                    check = True
                    break
            if (check == False):
                alphabet.append([num, len(alphabet)+1])
    length = len(alphabet)
    for i in range(length):
        alphabet[i][1] = alphabet[i][1]/length
    return alphabet

def getProcessedWord(word, max_length):
    int_arr = []
    padding = [0 for i in range(max_length - len(word))]
    for letter in word:
        int_arr.append(ord(letter))
    int_arr += padding
    return int_arr

def applyDistribution(arr):
    for i in range(len(arr)):
        for x in range(len(arr[i][0])):
            for j in range(len(alphabet)):
                if arr[i][0][x] == alphabet[j][0]:
                    arr[i][0][x] = alphabet[j][1]
    return arr


def readInExamples():
    try:
        _s_pos = open("nn_train_regex+.txt", "r")
        _s_neg = open("nn_train_regex-.txt", "r")
        _u_pos = open("nn_test_regex+.txt", "r")
        _u_neg = open("nn_test_regex-.txt", "r")
        s_pos = []
        s_neg = []
        u_pos = []
        u_neg = []
        s_pos = [line.rstrip('\n') for line in _s_pos]
        s_neg = [line.rstrip('\n') for line in _s_neg]
        u_pos = [line.rstrip('\n') for line in _u_pos]
        u_neg = [line.rstrip('\n') for line in _u_neg]
        _s_pos.close()
        _s_neg.close()
        _u_pos.close()
        _u_neg.close()
    except():
        print("File not found!")
        exit()
    max_length = findMaxLength(s_pos)
    if max_length < findMaxLength(s_neg):
        max_length = findMaxLength(s_neg)
    if max_length < findMaxLength(u_pos):
        max_length = findMaxLength(u_pos)
    if max_length < findMaxLength(u_neg):
        max_length = findMaxLength(u_neg)
    pos_train = []
    for x in s_pos:
        int_arr = getProcessedWord(x, max_length)
        pos_train.append([int_arr, 1])
    neg_train = []
    for x in s_neg:
        int_arr = getProcessedWord(x, max_length)
        neg_train.append([int_arr, 0])
    pos_test = []
    for x in u_pos:
        int_arr = getProcessedWord(x, max_length)
        pos_test.append([int_arr, 1])
    neg_test = []
    for x in u_neg:
        int_arr = getProcessedWord(x, max_length)
        neg_test.append([int_arr, 0])
    return pos_train, neg_train, pos_test, neg_test, max_length


p_train, n_train, p_test, n_test, max_length = readInExamples()
net = NeuralNetwork(max_length)
alphabet = (getAlphabet(p_train, n_train, p_test, n_test))
p_train = applyDistribution(p_train)
n_train = applyDistribution(n_train)
p_test = applyDistribution(p_test)
n_test = applyDistribution(n_test)
np_train = p_train + n_train
random.shuffle(np_train)
training_set_input = np.array([np_train[0][0]])
training_set_output = np.array([np_train[0][1]])
np_train = np_train[1:]
for i in np_train:
    training_set_input = np.append(training_set_input, [i[0]], axis = 0)
    training_set_output = np.append(training_set_output, [i[1]], axis = 0)
training_set_output = training_set_output.T
np_test = p_test + n_test
random.shuffle(np_test)
testing_set_input = np.array([np_test[0][0]])
testing_set_output = np.array([np_test[0][1]])
np_test = np_test[1:]
for i in np_test:
    testing_set_input = np.append(testing_set_input, [i[0]], axis = 0)
    testing_set_output = np.append(testing_set_output, [i[1]], axis = 0)
testing_set_output = testing_set_output.T


net.train(training_set_input, training_set_output, epochs)
i = 0
for x in testing_set_input:
    print(net.through(np.array(x)))
