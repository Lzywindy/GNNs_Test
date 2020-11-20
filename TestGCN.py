import torch
from torch import nn

in_features = 3
out_features = 3
N = 6 # 节点数目
W_edge = nn.Parameter(torch.zeros(size=(N, N)))
nn.init.xavier_uniform_(W_edge, gain=1.414)
Nodes_Test = nn.Parameter(torch.zeros(size=(in_features,N)))
nn.init.xavier_uniform_(Nodes_Test.data, gain=1.414)
W_next = torch.div(W_edge + torch.transpose(W_edge,0,1),2)
print(W_next)
print(Nodes_Test)
result = torch.mm(Nodes_Test,W_next)
print(result)

# 这个是个无向图卷积
# 训练可以使用梯度下降进行计算（pytorch中的方法都行）
# 采用的是空域卷积的模式
# 但是只需要输入顶点就可以进行计算
# 正如大家所见，图卷积拥有一定的局限性（比如顶点数目必须固定）
# 因此在卷积的过程中，势必只能学习N个顶点之间的关系
# node_features是一个N个顶点，每个顶点拥有N_features个特征的顶点
class GCN:
    def __init__(self,node_count:int, alpha:float):
        self.__node_count = node_count
        self.__W_edge = nn.Parameter(torch.zeros(size=(node_count, node_count)))
        self.__alpha = alpha
        self.__leakyrelu = nn.LeakyReLU(self.alpha)
    def forward(node_features):
        return leakyrelu(torch.mm(node_features,torch.div(self.__W_edge + torch.transpose(self.__W_edge,0,1),2)))