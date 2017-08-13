# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 16:23:58 2017
@author: Wanning Sun
输入百度高级搜索财新网结果，通过pandas排序输出txt文本，按时间升序
"""

import csv
import pandas as pd

def write_csv():
    f = open(r'/home/sun/pys/pachong/apply/caixin_all.txt')
    news_list = f.readlines()
    f.close()
    
    csvfile = file('csvtest.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['time', 'title','titlecomment', 'content'])
    
    for news in news_list:
        #print news
        news = news.strip('\n')
        one_piece = news.split('\t')
        writer.writerow(one_piece)
        print '111'
    csvfile.close()       
def newsSort():
    date_sort = pd.read_csv(r'/home/sun/pys/pachong/apply/csvtest.csv',index_col='time')
    date_sort = date_sort.sort_index(ascending=True)
    print date_sort
    date_sort.to_csv('caixin_sorted.txt',sep='\t') 
    #print date_sort[0][0]
    return date_sort
if __name__ == "__main__":
    write_csv()
    date_sort = newsSort()
    