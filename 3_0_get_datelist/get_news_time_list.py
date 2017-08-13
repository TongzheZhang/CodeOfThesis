# -*- coding: utf-8 -*-
"""
Created on Thu Mar 23 10:08:58 2017

@author: Richard
"""

import pandas as pd
import numpy as np

'''读入新闻'''
f = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\news_result_bf.txt')
news_list = f.readlines()
f.close()
for news in news_list:
    datef = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\news_time_list.txt', 'a')
    datef.write('\n' + news.split('\t')[0])
    datef.close()