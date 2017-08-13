# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 14:30:54 2017
得到Y值，在这里也就是股价增量
@author: Richard
"""
import pandas as pd
import scipy.io as sio
'''读取日期列表'''
t = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\datelist.txt')
datelist = t.readlines()
final_date = []
for i in range(0,len(datelist)):
    final_date.append(datelist[i].strip('\n'))
'''得到股价的日期'''
stocks = pd.read_csv(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\test_price.csv',index_col='date')
stocks = stocks.sort_index(ascending=True)
stocks = pd.DataFrame({"price": stocks.ix[:,'close']})
#计算
stocks_return = (stocks.shift(-1)['price']-stocks['price'])/stocks['price']
stocks_return = pd.DataFrame({"return": stocks_return})
'''去除回报为空的行'''
stocks_not_null = stocks_return[stocks_return["return"].notnull()]
print stocks_not_null.head()

all_incre = []
num = 0
for i in final_date:
    num = num + 1 
    all_incre.append(stocks_not_null[stocks_not_null.index==i]['return'].tolist()[0])
sio.savemat(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\y_incre.mat',{'y_incre':all_incre})