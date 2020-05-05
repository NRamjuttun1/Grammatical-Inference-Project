import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import random

use_gpu = False
learning_rate = 1
epochs = 1
batch_size = 10
func = F.relu
loss_fn = nn.BCELoss

class Net(nn.Module):

    def __init__(self, max_length):
        super().__init__()
        self.fc1 = nn.Linear(max_length, 48, bias = False)
        self.fc2 = nn.Linear(48, 16, bias = False)
        self.fc3 = nn.Linear(16, 8, bias = False)
        self.fc4 = nn.Linear(8, 2, bias = False)
        self.fc5 = nn.Linear(2, 1, bias = False)

    def forward(self, x):
        x = func(self.fc1(x))
        x = func(self.fc2(x))
        x = func(self.fc3(x))
        x = func(self.fc4(x))
        x = self.fc5(x)
        return F.log_softmax(x, dim=1)

class words_dataset(Dataset):

    def __init__(self, data, target):
        self.data = data
        self.target = target

    def __getitem__(self, index):
        return self.data[index], self.target[index]

    def __len__(self):
        return len(self.data)

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

train_x = []
train_y = []
for x in train:
    train_x.append(x[0])
    new_target = x[1]
    #train_y.append(F.log_softmax(new_target.view(-1, len(new_target)*1), dim=1))
    train_y.append(new_target)
training_set = words_dataset(train_x, torch.FloatTensor(train_y))
data_loader = DataLoader(dataset = training_set, batch_size = 10, shuffle = True)
data_loader_iter = iter(data_loader)
net = Net(max_length)
optimizer = optim.Adam(net.parameters(), lr = learning_rate)


for epoch in range(epochs):
    for data in data_loader:
        x, y = data
        net.zero_grad()
        output = net(x.view(-1, max_length))
        #y = F.log_softmax(y.view(len(y), 1), dim=1)
        loss = loss_fn()(output, y)
        loss.backward()
        optimizer.step()
        print(loss)
