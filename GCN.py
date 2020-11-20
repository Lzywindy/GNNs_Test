import torch
from torch import nn

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
        nn.init.xavier_uniform_(__W_edge, gain=1.414)
        self.__alpha = alpha
        self.__leakyrelu = nn.LeakyReLU(self.alpha)
    def forward(self,node_features):
        return self.__leakyrelu(torch.mm(node_features,torch.div(self.__W_edge + torch.transpose(self.__W_edge,0,1),2)))

# 这个是个无向图卷积（这个是一个基于特征压缩的GCN）
# 这个GCN是可以扩充或压缩节点特征（单纯变换可以来做残差模块）
# 训练可以使用梯度下降进行计算（pytorch中的方法都行）
# 采用的是空域卷积的模式
# 但是只需要输入顶点就可以进行计算
# 正如大家所见，图卷积拥有一定的局限性（比如顶点数目必须固定）
# 因此在卷积的过程中，势必只能学习N个顶点之间的关系
# node_features是一个N个顶点，每个顶点拥有N_features个特征的顶点
class GCN_CompressFeatures:
    def __init__(self,node_count:int,input_feature_N:int,output_feature_N:int, alpha:float):
        self.__node_count = node_count
        self.__feature_compress_activition = nn.ELU(0.3)
        self.__W_feature_compress = nn.Parameter(torch.zeros(size=(input_feature_N, output_feature_N)))
        nn.init.xavier_uniform_(__W_feature_compress, gain=1.414)
        self.__W_edge = nn.Parameter(torch.zeros(size=(node_count, node_count)))
        nn.init.xavier_uniform_(__W_edge, gain=1.414)
        self.__alpha = alpha
        self.__leakyrelu = nn.LeakyReLU(self.alpha)
    def forward(self,node_features):
        feature_compress = self.__feature_compress_activition(torch.mm(self.__W_feature_compress,node_features))
        return self.__leakyrelu(torch.mm(feature_compress,torch.div(self.__W_edge + torch.transpose(self.__W_edge,0,1),2)))
