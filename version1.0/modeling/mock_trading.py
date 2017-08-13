# -*- coding: utf-8 -*-
"""
Created on Thu Dec 22 15:08:10 2016
输入预测表格：日期和预测值，初始现金1000元，可融资或融券，通过交易策略高于1%买入，低于1%卖出，最后看持有的组合价值
现金加股票价值
@author: Richard
"""
import numpy as np
import pandas as pd

def mock_trading(pred_file = 'pred_result.txt',pricename = 'test_price.csv'):
    f = open(pred_file)
    predlines = f.readlines()
    startdate = predlines[0].split('\t')[0]
    stocksdata = pd.read_csv(pricename,index_col='date')
    stocksdata = stocksdata.sort_index(ascending=True)[startdate:]
    stocksdata = pd.DataFrame({"price": stocksdata.ix[:,'close'],
                           "cash":1000,
                           "stocks":0,
                           "profile":1000})
    #stocks.at['2016-08-08','Cash'] = 9999#用于改变值
    #print stocks 
    cash = 1000
    stocks = 0
    profile = 1000
    for index,row in stocksdata.iterrows():
        for deal in predlines:
            tempdate,tempreturn = deal.split('\t')
            #print '这里有改变：',tempdate,tempreturn

            if index == tempdate:
                print tempreturn
                if float(tempreturn) > 0.0:
                    print '大于0'
                    if stocks <= 200:
                        stocks += 100
                        cash -= 100*row['price']
                else:
                    print '小于0'
                    if stocks >= -200:
                        stocks -= 100
                        cash += 100*row['price']
            
        profile =cash + stocks*row['price']
        stocksdata.at[index,'cash'] = cash
        stocksdata.at[index,'stocks'] = stocks
        stocksdata.at[index,'profile'] = profile
        #print stocksdata.loc[index],cash,stocks,profile
    print stocksdata

                           

    print 'end of function(mock_trading)'
    
    
if __name__ == '__main__':
    print 'start'
    
    mock_trading()
