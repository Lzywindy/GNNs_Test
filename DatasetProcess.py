#import time
#import numpy as np
#import pickle as pk
#import pandas as pd
#import threading
#import Utils as ut

#total_record_usefuldata = 12
#SID_local = 1
#timestamp_local = 0
#avg_speed_local = total_record_usefuldata - 1
#avg_occupancy_local = total_record_usefuldata - 2
#total_flow_local = total_record_usefuldata - 3
#time_str = r'2012_01_01'
#str_adj_mx = r'F:\PyFile\adj_mx.pkl'
#def SpiltData2List(line:str):
#    line = line.split(',',total_record_usefuldata)
#    timeArray = time.strptime(line[timestamp_local], "%m/%d/%Y %H:%M:%S")
#    if line[total_flow_local] == '':
#        t_0 = 0
#    else:
#        t_0 = int(line[total_flow_local])
#    if line[avg_occupancy_local] == '':
#        t_1 = 0
#    else:
#        t_1 = float(line[avg_occupancy_local])
#    if line[avg_speed_local] == '':
#        t_2 = 0
#    else:
#        t_2 = float(line[avg_speed_local])
#    return [int(line[SID_local]),time.mktime(timeArray),[t_0,t_1,t_2]]

#def addtwodimdict(thedict:dict, key_a, key_b, val):
#    if key_a in thedict:
#        thedict[key_a].setdefault(key_b,val)
#    else:
#        thedict.setdefault(key_a,{key_b,val})

#f_path = r'E:\DCRNN-master\DCRNN-master\data\sensor_graph\adj_mx.pkl'
#with open (f_path, 'rb') as f: #打开文件
#    aa = pk.load(f,encoding='latin1')
#    print(aa)

#array_row = list()
#array_col = list()
#array_data = list()
#f_path_s = r'E:\PeMSD7-2012\原始数据包'
#f_name_sel = r'\d07_text_station_5min_'
#f_exname = '.txt'
#f_path = f_path_s + f_name_sel + time_str + f_exname
#f = open(f_path)
#try:
#    content = f.read()
#finally:
#    f.close()
#lines = content.split('\n')
#lines = [inf for inf in lines if inf != '']
#for line in lines:
#    data = ut.SpiltData2List(line)
#    if data[1] not in array_row:
#        array_row.append(data[1])
#    if data[0] not in array_col:
#        array_col.append(data[0])
#    array_data.append(data)
#np.save('F:\PyFile\data_row.npy', array_row)
#np.save('F:\PyFile\data_col.npy', array_col)
#np.save('F:\PyFile\data_data.npy', array_data)
#array_row = np.load('F:\PyFile\data_row.npy',allow_pickle=True)
#array_col = np.load('F:\PyFile\data_col.npy', allow_pickle=True)
#array_data = np.load('F:\PyFile\data_data.npy', allow_pickle=True)
#array_thread = list()


#df = pd.DataFrame(data=None,index=array_row,columns=array_col)

#def thread_fun(param:list):
#    df.loc[param[1],param[0]] = param[2]

#for item in array_data:
#    thread = threading.Thread(target=thread_fun,args=(item,))
#    array_thread.append(thread)
#    thread.start()
#for t in array_thread:
#    t.join()
   
#df.to_pickle(r'E:\PeMSD7-2012\原始数据包' + f_name_sel + time_str + '.pkl')
#print(df)
#array_col = np.load('F:\PyFile\data_col.npy', allow_pickle=True)
#adj_aa_df = pd.DataFrame(data=[[0] * (len(array_col) )] * (len(array_col)
#),index=array_col,columns=array_col,dtype=float)
#adj_aa_df.to_pickle(str_adj_mx)
#adj_aa_df = pd.read_pickle(str_adj_mx)
import torch
from torch import nn

in_features = 3
out_features = 3
N = 6
with torch.no_grad():
    weight = nn.Parameter(torch.ones(size=(N, N)))
alpha = 0.2
leakyrelu = nn.LeakyReLU(alpha)
elu = torch.nn.ELU()
W = nn.Parameter(torch.zeros(size=(in_features, out_features)))
nn.init.xavier_uniform_(W.data, gain=1.414)
A = nn.Parameter(torch.zeros(size=(2 * out_features, 1)))
nn.init.xavier_uniform_(A.data, gain=1.414)
inp = nn.Parameter(torch.zeros(size=(N, in_features)))
nn.init.xavier_uniform_(inp.data, gain=1.414)
def Function(inp,weight):
    h = torch.mm(inp,W)
    weight.requires_grad = False
    a_input = torch.cat([h.repeat(1, N).view(N * N, -1), h.repeat(N, 1)],dim=1).view(N, N, 2 * out_features)
    e = leakyrelu(torch.matmul(a_input, A).squeeze(2))
    e_norm_2 = torch.norm(e,p=2,dim=1,keepdim=True)
    attention_norm_2ed = torch.div(torch.mul(e,weight),torch.where(e_norm_2 == 0,torch.ones_like(e_norm_2),e_norm_2).repeat(1, N).view(N , N))
    h_prime = elu(torch.matmul(attention_norm_2ed, h))
    return h_prime,attention_norm_2ed
print(weight)
nodes_h,weight = Function(inp,weight)
print(W)

U,S,V = torch.svd(W)
S = torch.diag(S)
#print(U)
#print(S)
#print(V)
W = torch.mm(U,S)
#W.no_grad()

#print(W.numpy())
#print(nodes_h)
print(weight.requires_grad)

#print(h)
#print(e)
#print(e_norm_2)
#print(n)