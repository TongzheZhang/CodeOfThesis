# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 11:33:40 2017
计算特征
布林线指标，
@author: Richard
"""

import pandas as pd
import scipy.io as sio 
def cal_firm_features():
    #read data
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
    date_set = {}.fromkeys([ line.rstrip().decode('utf8') for line in open('datelist.txt') ])

    del_list = []
    for i in range(0,len(final_result)):
        if final_result.index[i] not in date_set:
            del_list.append(final_result.index[i])
    save_result = final_result.drop(del_list,axis=0)
    
    save_result.to_csv('num_features.csv')  
    result_list = save_result.values
    sio.savemat('firm_features.mat', {'firm_features': result_list})