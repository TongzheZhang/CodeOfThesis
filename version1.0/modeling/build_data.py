# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 16:52:42 2016
得到数据集,通过把日期和差价增量和新闻合在一起，取价格和新闻事件交集（因为假设贴吧每天都会有），合成data.txt，共221天
并输出混合的日期（即可以使用的日期）
为什么不把贴吧接在后面？因为贴吧不是按天排的。。。
@author: Richard
"""

import pandas as pd
import numpy as np

'''读入新闻'''
f = open('test_news.txt')
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
t = open('test_tieba.txt')
tieba = t.readlines()
tieba_split = []
for i in range(0,len(tieba)):
    tieba_split.append(tieba[i].split('\t'))#有六个条目，日期，阅读数，点赞数，题目，帖子，回帖
print '贴吧的大小:',len(tieba_split),len(tieba_split[0])

'''得到股价的日期'''
stocks = pd.read_csv(r'test_price.csv',index_col='date')
stocks = stocks.sort_index(ascending=True)
stocks = pd.DataFrame({"price": stocks.ix[:,'close']})
#计算
stocks_return = (stocks.shift(-1)['price']-stocks['price'])/stocks['price']
stocks_return = pd.DataFrame({"return": stocks_return})

stocks_not_null = stocks_return[stocks_return["return"].notnull()]#去除回报为空的行
print stocks_not_null.head()
all_date = []
for date in stocks_not_null.index.tolist():
    all_date.append(date[5:])
price_date = set(all_date)

'''混合两个共有的日期，并得到训练集和测试集'''
print '价格和新闻各有多少天',len(price_date),len(news_date)
final_date = price_date & news_date
print '混合的天数：',len(final_date)
final_combined = []
'''把新闻和差价结合'''
all_return = []
all_news = []
all_tobewrite_date = []
all_tieba = []
lastdate = ''
tempnews = ''
tempdate = ''
tempprice = 0.0
temptieba = ''
for i in news_split:    
    if i[0] in final_date:

        if i[0][0] == '1':
            tempdate = '2015-'+i[0]
        else:
            tempdate = '2016-'+i[0]

        if tempdate != lastdate: 
            all_return.append(tempprice)
            all_news.append(tempnews)
            all_tobewrite_date.append(lastdate)
            all_tieba.append(temptieba)
            tempnews = ''
            temptieba = ''
        tempprice = stocks_not_null[stocks_not_null.index==tempdate]['return'].tolist()[0]
        temptieba = ''    
        '''
        for idx,n in enumerate(tieba_split):
            if n[0] == i[0]:
                temptieba += temptieba + n[3] 
        '''
        tempnews = tempnews + i[3]+' '+i[4] +' '
        
        lastdate = tempdate
all_return.append(tempprice)
all_news.append(tempnews)
all_tobewrite_date.append(lastdate)
all_return = all_return[1:]
all_news = all_news[1:]
all_tobewrite_date = all_tobewrite_date[1:]
'''
for i in tieba_split:
    for idx,n in enumerate(all_tobewrite_date):
        if i[0] == n[5:]:
            all_tieba[idx] = all_tieba[idx].join(i[3]+' '+i[4]+' '+i[5]+' ')
print '帖子一共多少：',len(all_tieba)
'''
print '-----'
print len(all_return)
print len(all_news)
print len(all_tobewrite_date)
print len(all_tieba)#后面好像没用
#print all_news[-1]
print stocks_not_null.tail()
print stocks_not_null.head()
print '09-30' in final_date

print len(all_news)
f = open('data.txt','w')
datef = open('datelist.txt', 'w')
#写入日期，真实回报值，新闻串接
for i in range(0,len(final_date)):
    f.write(all_tobewrite_date[i]+'\t'+str(all_return[i])+'\t'+all_news[i]+'\n')
    datef.write(all_tobewrite_date[i]+'\n')
f.close()
datef.close()

    

    
    