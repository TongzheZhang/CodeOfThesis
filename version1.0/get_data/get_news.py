# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 10:22:32 2016

@author: Tongzhe Zhang
东方财富新闻，得到新闻的标题，评论等
"""

#-*- coding:utf-8 -*-
import urllib
import urllib2
import re


# 连接http://guba.eastmoney.com/news,000651,572081295.html

class News:
    def __init__(self,baseUrl,date,reading,commenting):
        self.baseUrl = baseUrl
        self.date = date
        self.reading = reading
        self.commenting = commenting
        
    # 传入页码，获取网页源代码
    def getPage(self):
        try:
            # 拼接，地址 + 页数
            url = self.baseUrl
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read()
        except Exception,e:# 处理异常
            print e
    # 获取标题
    def getTitle(self):
        html = self.getPage()

        #找到标题和内容
        reg = re.compile(r'<div id="zwconttbt">(.*?)</div>',re.S)#正则表达式中，“.”的作用是匹配除“\n”以外的任何字符
        titlecomment = re.compile(r'<div id=[\'\"]zw_body[\'\"].?>(.*?)\[点击查看原文\]</b></a></div>',re.S)
        
        items = re.findall(reg,html)#正则表达式 re findall 方法能够以列表的形式返回能匹配的子串。
        titlecomment = re.findall(titlecomment,html)
       
        #remove all tags

        removeAll = re.compile('<.*?>')#去除链接

        items[0] = re.sub(removeAll,"",items[0])
        if len(titlecomment) == 1:
            titlecomment = re.sub(removeAll,"",titlecomment[0])
        else:
            print '网页不规范'
            titlecomment = '没有内容'
        f = open('news.txt','a') # 文件名最好是英文，中文识别不了
        f.write('\n'+self.date + '\t' +str(self.reading)+'\t'+str(self.commenting)+'\t'+ items[0].strip()+'\t'+titlecomment.strip() +'\t')
        f.close()
        
        #print items[0].strip()
        #print titlecomment[0].strip()
        return items
        

        
    def getContent(self):
        html = self.getPage()
        reg = re.compile(r'<div class="zwlitext stockcodec">(.*?)</div>',re.S)
        req = re.findall(reg,html)
        emoji = re.compile(r'<img src.*? title="(.*?)"/>',re.S)
        removeAll = re.compile('<.*?>')#去除所有标签
        removeEmoji = re.compile('<img src.*?/>')#去除表情
        
        for i in req:            
            em = re.findall(emoji,i)
            i = re.sub(removeEmoji,"",i)
            i = re.sub(removeAll,"",i)
            for a in range(len(em)):
                i = em[a] + ' ' + i
            
            #print i
            
            f = open('news.txt','a')# 此处是写入正文内容，所以用a
            f.write(i.strip()+' ')
            f.close()
            
        


#daseURL = 'http://guba.eastmoney.com/news,600848,429878160.html'
if __name__ == "__main__":    
    baseURL = 'http://guba.eastmoney.com/news,000651,571985483.html' 
    ls = News(baseURL,'11-11',1,1)
    print "爬虫已启动..."

    ls.getTitle()
    ls.getContent()
    
    print "本页爬虫结束"