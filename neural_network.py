import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import random

use_gpu = False
learning_rate = 0.1
epochs = 50
batch_size = 10

class Net(nn.Module):

    def __init__(self, max_length):
        super().__init__()
        self.fc1 = nn.Linear(max_length, 16, bias = False)
        self.fc2 = nn.Linear(16,8, bias = False)
        self.fc3 = nn.Linear(8,1, bias = False)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = (self.fc3(x))
        return F.log_softmax(x, dim=1)


def set_gpu():
    if (torch.cuda.is_available()):
        device = torch.device("cuda:0")
    else:
        device = torch.device("cpu")
    return device

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
    max_length = 0
    pos_train_set = []
    for x in s_pos:
        if len(x) > max_length:
            max_length = len(x)
        int_arr = []
        for letter in x:
            int_arr.append(ord(letter))
        pos_train_set.append([int_arr, 1])
    neg_train_set = []
    for x in s_neg:
        if len(x) > max_length:
            max_length = len(x)
        int_arr = []
        for letter in x:
            int_arr.append(ord(letter))
        neg_train_set.append([int_arr, 0])
    pos_test_set = []
    for x in u_pos:
        if len(x) > max_length:
            max_length = len(x)
        int_arr = []
        for letter in x:
            int_arr.append(ord(letter))
        pos_test_set.append([int_arr, 1])
    neg_test_set = []
    for x in u_neg:
        if len(x) > max_length:
            max_length = len(x)
        int_arr = []
        for letter in x:
            int_arr.append(ord(letter))
        neg_test_set.append([int_arr, 0])
    train = pos_train_set + neg_train_set
    random.shuffle(train)
    for x in train:
        for i in range(max_length - len(x[0])):
            x[0].append(0)
        x[0] = torch.Tensor(x[0])
    test = pos_test_set + neg_test_set
    random.shuffle(test)
    for x in test:
        for i in range(max_length - len(x[0])):
            x[0].append(0)
        x[0] = torch.Tensor(x[0])
    return train, test, max_length



if use_gpu:
    device = set_gpu()
else:
    device = torch.device("cpu")


train, test, max_length = readInExamples()

net = Net(max_length)
optimizer = optim.Adam(net.parameters(), lr=learning_rate)

check = False
training_set = []
while(not check):
    if len(train) > batch_size:
        train_batch = train[0:batch_size]
        train = train[batch_size:]
        training_set.append(train_batch)
    elif (not len(train) == 0):
        training_set.append(train)
        check = True
    else:
        check = True

for epoch in range(epochs):
    for batch in training_set:
        for data in batch:
            input = data[0]
            target = torch.tensor([data[1]])
            output = net(input.view(-1, max_length*1))
            loss = F.mse_loss(output, target)
            net.zero_grad()
            loss.backward()
            optimizer.step()
            print(loss)
