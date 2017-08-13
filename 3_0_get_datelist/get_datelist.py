# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 11:05:21 2017
计算新闻，价格，贴吧信息的都共同存在的日期信息
@author: Richard
"""

import pandas as pd
import numpy as np

'''读入新闻'''
f = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\test_news.txt')
news = f.readlines()
news.reverse()
news_split = []
for i in range(0,len(news)):
    news_split.append(news[i].split('\t'))#有六个条目，日期，阅读数，点赞数，题目，新闻，回复

all_date = []
for i in news_split:
    all_date.append(i[0])
news_date = set(all_date)

'''读入贴吧'''
t = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\test_tieba.txt')
tieba = t.readlines()
tieba_split = []
for i in range(0,len(tieba)):
    tieba_split.append(tieba[i].split('\t'))#有六个条目，日期，阅读数，点赞数，题目，帖子，回帖
all_date = []
for i in tieba_split:
    all_date.append(i[0])
tieba_date = set(all_date)
print '贴吧的大小:',len(tieba_split),len(tieba_split[0])
print '贴吧的日期有多少个',len(tieba_date)

'''得到股价的日期'''
stocks = pd.read_csv(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\test_price.csv',index_col='date')
stocks = stocks.sort_index(ascending=True)
stocks = pd.DataFrame({"price": stocks.ix[:,'close']})
#计算
stocks_return = (stocks.shift(-1)['price']-stocks['price'])/stocks['price']
stocks_return = pd.DataFrame({"return": stocks_return})
'''这里可以改进，不用去掉最后一行，获得股价数据时多获取一行就可以了'''
stocks_not_null = stocks_return[stocks_return["return"].notnull()]#去除回报为空的行
print stocks_not_null.head()
all_date = []
for date in stocks_not_null.index.tolist():
    all_date.append(date[5:])
price_date = set(all_date)

'''混合两个共有的日期，并得到训练集和测试集'''
print '价格和新闻和贴吧各有多少天',len(price_date),len(news_date),len(tieba_date)
final_date = price_date & news_date & tieba_date
print '混合的天数：',len(final_date)


'''把日期的格式稳定结合'''
all_tobewrite_date = []
lastdate = ''
tempdate = ''

for i in news_split:    
    if i[0] in final_date:

        #if i[0][0] == '1':
        #    tempdate = '2015-'+i[0]
        #else:
        tempdate = '2016-'+i[0]

        if tempdate != lastdate: 
            all_tobewrite_date.append(lastdate)        
        lastdate = tempdate


all_tobewrite_date.append(lastdate)
all_tobewrite_date = all_tobewrite_date[1:]

print '-----'
print len(all_tobewrite_date)
print '09-30' in final_date
print '2015-10-08' in final_date
print '2016-10-08' in final_date
print '10-08' in final_date

'''将日期写入文件'''
datef = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\datelist.txt', 'w')
#写入日期，真实回报值，新闻串接
for i in range(0,len(final_date)):
    if i != len(final_date)-1:
        datef.write(all_tobewrite_date[i]+'\n')
    else:
        datef.write(all_tobewrite_date[i])
datef.close()

split_num = int(round(len(all_tobewrite_date)*0.8))
print '我是训练集有多少个！！！！！！！',split_num
print '我是测试集有多少个！！！！！！！',len(all_tobewrite_date)-split_num