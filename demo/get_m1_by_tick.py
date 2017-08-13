# -*- coding: utf-8 -*-
"""
Created on Mon Mar 06 16:48:04 2017
根据tick数据计算分钟线的示例
@author: Richard
"""

import tushare as ts
import pandas as pd

df = ts.get_tick_data('600000', date='2016-01-05')
calData = ts.get_h_data('600000',start='2015-10-01',end='2016-12-31') #在这修改股票代码，前复权,从今天数前一年

df['time'] = '2016-10-28 ' + df['time']
df['time'] = pd.to_datetime(df['time'])
df = df.set_index('time') 

#进行采样得到开始的价格，最高价，最低价，结束的价格
price_df = df['price'].resample('1min').ohlc()
price_df = price_df.dropna()#删除空值
print price_df.head(10)
print price_df.tail(10)