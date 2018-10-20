
import torch
import torch.nn as nn
import torch.nn.functional as Function
import numpy as np
from functools import reduce
from torch.autograd import Variable


learning_rate = 0.005
dtype = torch.float
device = torch.device("cpu")
# device = torch.device("cuda:0") # Uncomment this to run on GPU

input_width, output_width = 102, 1
# hidden_layers_width = [500, 100, 100, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 55, output_width]
hidden_layers_width = [100, 100, 100, output_width]

def make_layers():
    last_width = input_width
    layers = []

    for width in hidden_layers_width:
        layers.append(nn.Linear(last_width, width))
        last_width = width
    return layers

class NeuralNetwork(nn.Module):

    network = []
    predictions = torch.zeros(1, dtype = dtype, requires_grad=True)

    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.network = make_layers()

    def forward(self, input):
        vector = input
        for layer in self.network:
            vector = Function.relu(layer(vector))
        output = vector
        return output

    def run_decision(self, board_features):
        vector = board_features
        prediction = self(board_features)
        torch.cat((self.predictions, prediction))

    def evaluate(self, board_features):
        with torch.no_grad():
            return self(board_features)

    def get_reward(self, reward):
        episode_length = len(self.predictions)
        y = torch.ones(episode_length, dtype=dtype) * reward
        loss = torch.abs(y - self.predictions).sum()

        loss.backward()
        self.zero_grad()
        self.predictions = torch.zeros(1, dtype = dtype, requires_grad=True)
        # kalla a predictions.sum til ad kalla bara einu sinni a
        # loss.backward()
