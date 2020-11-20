
#import torch

#glu_unit = torch.nn.GLU()
#_input=torch.randn(4,2)
#_output=glu_unit(_input)
#print(_input)
#print(_output)
#f_path = 'E:\PeMSD7-2012\原始数据包\d07_text_station_5min_2012_01_01.txt'
#f = open(f_path)
#try:
#    content = f.read()
#finally:
#    f.close()
#lines=content.split('\n')
#lines=[inf for inf in lines if inf!='']
#line=lines[0].split(',',12)
#line.remove(line[12])
#print(line)
#print(content)

#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt
#v0 = 0
#C = 0.865
#dense = 1.293
#S = 1
#delta_t = 0.001
#target_t = int(10 / delta_t)
#v = v0
#g = 9.81
#t = 0
#s = 0
#m = 100
#points_t=[]
#points_a=[]
#points_v=[]
#points_s=[]
#for i in range(0,target_t):
#   t = t + delta_t
#   a = g - (C * dense * S * v / (2 * m))
#   v = v + a * delta_t   
#   s = s + v * delta_t
#   points_t.append(t)
#   points_a.append(a)
#   points_v.append(v)
#   points_s.append(s)

#plt.title('Result Analysis')
#plt.plot(points_t, points_a, color='red', label='Acceleration(m/s^2)')
#plt.plot(points_t, points_v,  color='green', label='Speed(m/s)')
#plt.plot(points_t, points_s, color='skyblue', label='Height(m)')
#plt.legend()
#plt.show()


