# -*- coding: utf-8 -*-
"""
Created on Sat Jan 28 18:01:59 2017
把预测值和日期转化为txt格式
@author: Richard
"""
import scipy.io as sio
#%%载入预测的价格
price = sio.loadmat('pred_price.mat')
priceget = price['pred_price']
#%%载入日期列表，并读取测试集部分
f = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\datelist.txt')
lines = f.readlines()
lines = lines[177:]
print len(lines)
#%%写入预测文本
w = open(r'E:\study\master of TJU\0Subject research\code\Important\5_1_mock_trading\pred_result.txt','w')
for i in range(0,44):
    w.write(lines[i].strip()+'\t'+str(priceget[i,0])+'\n')
w.close()