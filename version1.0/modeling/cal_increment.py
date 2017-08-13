# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 15:25:59 2016

示例程序

处理股价，对应一个增量
输出股价的时间
@author: Richard
"""

import pandas as pd
import numpy as np
#得到估价复权后的价格,让新的价格在底下！
stocks = pd.read_csv(r'test_price.csv',index_col='date')
stocks = stocks.sort_index(ascending=True)
print '第一行的日期:',stocks.index[0]
print '最后一行日期:',stocks.index[-1]

stocks = pd.DataFrame({"price": stocks.ix[:,'close']})
print 
print stocks.head()
print stocks.tail()

stocks_return = (stocks.shift(-1)['price']-stocks['price'])/stocks['price']
stocks_return = pd.DataFrame({"return": stocks_return})
#stock_return = stocks['PRICE'].apply(lambda x: np.log(x) - np.log(x.shift(1))) # shift moves dates back by 1.

print stocks_return.head()
print stocks_return.tail()

'''
set_date = stocks_return['Date'].tolist().remove('2015-10-08')
print stocks_return['Date'].tolist()
'''


df_not_null = stocks_return[stocks_return["return"].notnull()]#去除回报为空的行
print len(stocks_return)
print len(df_not_null)
print '去掉了最后一天没有回报的日子'
print df_not_null.head()
print df_not_null.tail()
all_date = []
for date in df_not_null.index.tolist():
    #因为用一年的数据，但是跨年了，所以去掉了年份。
    all_date.append(date[5:])
print set(all_date)
