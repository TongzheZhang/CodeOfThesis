# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 11:33:40 2017
计算特征
布林线指标
添加min1的特征
@author: Richard
"""

import pandas as pd
import scipy.io as sio 
import numpy as np
import datetime
def cal_firm_features():
    #read data 这里面的数据是多用了几十天的数据，以保证数据的完整性
    stocks = pd.read_csv(r'test_price.csv',index_col='date')
    stocks = stocks.sort_index(ascending=True)
    print '第一行的日期:',stocks.index[0]
    print '最后一行日期:',stocks.index[-1]
    
    #get the price of stock
    stocksprice = pd.DataFrame({"price": stocks.ix[:,'close']})
    #get the volume of stock
    stocksvolume = pd.DataFrame({"volume": stocks.ix[:,'volume']})
    #get the amount of stock
    stocksamount = pd.DataFrame({"amount": stocks.ix[:,'amount']})
    
    #get daily_return of stock from yesterday
    stocks_return = (stocksprice['price']-stocksprice.shift(1)['price'])/stocksprice['price']
    stocks_return = pd.DataFrame({"return": stocks_return})
    #print stocks_return.head()
    #print stocks_return.tail()
    
    #get volatility
    volatility = pd.DataFrame({"vol": stocks_return.ix[:,'return']})
    volatility = pd.rolling_std(volatility,20)
    #print volatility.head()
    #print volatility.tail()
    
    #get momentum
    momentum = pd.DataFrame({"mom": stocksprice.ix[:,'price']})
    momentum = momentum/momentum.shift(19)-1.0

    #get bb_value
    bb_value = pd.DataFrame({"bb": stocksprice.ix[:,'price']})
    stdev = pd.rolling_std(bb_value,20)
    SMA = pd.rolling_mean(bb_value,20)
    bb_value = (stdev-SMA)/(2*stdev)
    
    final_data = pd.concat([stocksvolume,stocksamount,stocks_return,volatility,momentum,bb_value],axis = 1)
    
    #normalize
    final_data['volume'] = (final_data['volume']-final_data['volume'].mean())/final_data['volume'].std()
    final_data['amount'] = (final_data['amount']-final_data['amount'].mean())/final_data['amount'].std()
    final_data['vol'] = (final_data['vol']-final_data['vol'].mean())/final_data['vol'].std()
    final_data['mom'] = (final_data['mom']-final_data['mom'].mean())/final_data['mom'].std()
    final_data['bb'] = (final_data['bb']-final_data['bb'].mean())/final_data['bb'].std()
    
    
    #print final_data.head()
    #print final_data.tail()
    return final_data.dropna()
if __name__ == '__main__':
    print 'In the main function'
    
    final_result = cal_firm_features()
    
    '''读取日期列表'''
    t = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\date_list_min1.txt')
    datelist = t.readlines()
    all_date = []
    #去除年份和分钟
    for i in range(0,len(datelist)):
        all_date.append(datelist[i][:10].strip('\n'))
    
    save_result = []
    last_day = []
    #把相应天数的特征附在上面
    for i in range(0,len(all_date)):
        
        if all_date[i] in final_result.index:
            
            save_result = save_result + final_result.ix[all_date[i]].tolist()

        else:
            print 'i am not in firm_feature_list'
            timenow = datetime.datetime.strptime(all_date[i], "%Y-%m-%d")
            last_day = timenow
            while last_day.strftime("%Y-%m-%d") not in final_result.index:
                last_day = last_day + datetime.timedelta(days = -1)

            
            save_result = save_result + final_result.ix[last_day.strftime("%Y-%m-%d")].tolist()
   
    #reshape list
    save_result_reshape = np.array(save_result).reshape(len(all_date),6)
    sio.savemat(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\firm_features_min1.mat', {'firm_features': save_result_reshape})
    