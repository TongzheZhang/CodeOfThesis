# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 16:12:51 2017

@author: sun
"""
import pandas as pd
import scipy.io as sio
import datetime
import csv
'''读取日期列表'''
t = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\news_time_list.txt')
news_date_list = t.readlines()
t.close()
news_date = []
for i in range(0,len(news_date_list)):
    news_date.append(news_date_list[i].strip('\n'))
    
delta = datetime.timedelta(minutes=30)
delta_date = datetime.timedelta(days=1)
defer = []
for firtime in news_date:
    d=datetime.datetime.strptime(firtime,'%Y-%m-%d %H:%M:%S')
    n_minutes = d + delta
    sectime = n_minutes.strftime('%Y-%m-%d %H:%M:%S')   #获得第二个时间
    
    last_time = '2016-01-04 09:24:00'#初始化时间

    print firtime

    csv_reader = csv.reader(open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\price_min1.csv'))
    for row in csv_reader:
        time_format = datetime.datetime.strptime(row[0], '%Y/%m/%d %H:%M')
        row_format = time_format.strftime('%Y-%m-%d %H:%M:%S')      #统一时间形式
        
        '''找到第一个参考时间'''
        if last_time<= firtime <row_format:
            firtime = last_time
            fir_price = row[4]

        '''找到第二个参考时间'''
        if last_time< sectime <=row_format:
            if row_format.split()[1]>='09:30:00':
                sectime = row_format
                sec_price = row[4]
            else:   #如果时间不在开市时间内，取9:30
                sectime = row_format.split()[0] + ' 09:30:00'
                for low in csv_reader:
                    time_format2 = datetime.datetime.strptime(low[0], '%Y/%m/%d %H:%M')
                    low_format = time_format2.strftime('%Y-%m-%d %H:%M:%S')
                    if low_format == sectime:
                        sec_price = low[4]
                        break
            break        
        last_time = row_format
        
    deference = (float(sec_price)-float(fir_price))/float(fir_price)
    defer.append(deference)
print defer
sio.savemat(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\y_min1.mat',{'y_min1':defer})