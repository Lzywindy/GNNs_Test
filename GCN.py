import torch
from torch import nn

class GCN:
    def __init__(self,node_count:int, alpha:float):
        self.__node_count = node_count
        self.__W_edge = nn.Parameter(torch.zeros(size=(node_count, node_count)))
        self.__alpha = alpha
        self.__leakyrelu = nn.LeakyReLU(self.alpha)
    def forward(node_features):
        return leakyrelu(torch.mm(node_features,torch.div(self.__W_edge + torch.transpose(self.__W_edge,0,1),2)))
