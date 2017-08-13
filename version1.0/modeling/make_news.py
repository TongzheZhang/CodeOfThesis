# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 16:15:15 2016

示例程序

倒序读入新闻，和股价对应
得到date_list
@author: Richard
"""
import pandas as pd


f = open('test_news.txt')
news = f.readlines()
news.reverse()
print '最旧的新闻：',news[0]
print '最新的新闻：',news[-1]
print '共有：',len(news),'条新闻'
news_split = []
for i in range(0,len(news)):
    news_split.append(news[i].split('\t'))
print len(news_split[0])#有六个条目，日期，阅读数，点赞数，题目，新闻，回复

print news_split[0][0] == '10-01'#可以判断日期，最新日期应该是2015年10月1日
all_date = []
for i in news_split:
    all_date.append(i[0])
news_date = set(all_date)
print '11-06' in news_date
print len(news_date),'天有新闻'