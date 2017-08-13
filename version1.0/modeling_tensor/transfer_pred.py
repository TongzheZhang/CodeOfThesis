# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 18:01:59 2017
把预测值和日期转化为txt格式
@author: Richard
"""
import scipy.io as sio
price = sio.loadmat('pred_price.mat')
priceget = price['pred_price']

f = open('datelist.txt')
lines = f.readlines()

lines = lines[177:]
print len(lines)

w = open('pred_result.txt','w')
for i in range(0,44):
    
    w.write(lines[i].strip()+'\t'+str(priceget[i,0])+'\n')
    
w.close()