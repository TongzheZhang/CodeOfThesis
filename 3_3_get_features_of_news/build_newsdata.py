# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 11:24:02 2017
构建按天为一行的新闻文本库
@author: Richard
"""
'''读取日期列表'''
t = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\datelist.txt')
datelist = t.readlines()
final_date = []
for i in range(0,len(datelist)):
    final_date.append(datelist[i][5:].strip('\n'))
    
'''读入新闻'''
f = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\test_news.txt')
news = f.readlines()
news.reverse()#因为新闻也是从最近的日子开始的
news_split = []
for i in range(0,len(news)):
    news_split.append(news[i].split('\t'))#有六个条目，日期，阅读数，点赞数，题目，新闻，回复

#测试哪个日子存在
print '10-01' in final_date
print '2015-10-08' in final_date
print '10-08' in final_date

'''把同一天新闻合并'''
all_news = []
#all_tobewrite_date = []
lastdate = ''
tempnews = ''
tempdate = ''

for i in news_split:    
    if i[0] in final_date:
        #if i[0][0] == '1':
        #    tempdate = '2015-'+i[0]
        #else:
        tempdate = '2016-'+i[0]

        if tempdate != lastdate: 

            all_news.append(tempnews)
            #all_tobewrite_date.append(lastdate)
            tempnews = ''
        tempnews = tempnews + i[3]+' '+i[4] +' '        
        lastdate = tempdate

all_news.append(tempnews)
#all_tobewrite_date.append(lastdate)
all_news = all_news[1:]
#all_tobewrite_date = all_tobewrite_date[1:]

print '-----'
print '使用的新闻有几天的：',len(all_news)
f = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\newsdata.txt','w')

#每天的新闻串接
for i in range(0,len(final_date)):
    if i != len(final_date)-1:
        f.write(all_news[i]+'\n')#all_tobewrite_date[i]+'\t'+ 这是用来写入日期的     
    else:
        f.write(all_news[i])#all_tobewrite_date[i]+'\t'+ 这是用来写入日期的
f.close()


    
