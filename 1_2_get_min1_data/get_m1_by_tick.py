# -*- coding: utf-8 -*-
"""
Created on Mon Mar 06 16:48:04 2017
根据tick数据计算分钟线的示例
@author: Richard
"""

import tushare as ts
import pandas as pd

all_pd = []
calData = ts.get_k_data('600036', start='2016-01-01', end='2016-12-31',autype='qfq') 
#calData = ts.get_h_data('600036', start='2016-01-01', end='2016-12-31') 

for i in range(len(calData)):#list(calData.index):
    time_list = []
    one_date = calData.at[i,'date']
    print one_date
    df = ts.get_tick_data('600036', date=one_date)
    
    try:
        df['time'] = one_date + ' ' + df['time']
        df['time'] = pd.to_datetime(df['time'])
    except:
        print df
        continue
    df = df.set_index('time') 

    #进行采样得到开始的价格，最高价，最低价，结束的价格
    price_df = df['price'].resample('1min').ohlc()
    price_df = price_df.dropna()#删除空值
    all_pd.append(price_df)
    
    result=pd.concat(all_pd)
    result['SECCODE']='600036'
    result['SECNAME']='招商银行'
    result.rename(columns={'open':'STARTPRC', 'low':'LOWPRC', 'close':'ENDPRC', 'high':'HIGHPRC'}, inplace = True)

result.to_csv(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\price_min1.csv',index=True,encoding="gb2312")
