# -*- coding: utf-8 -*-
"""
Created on Mar 3 ,2017
@author: Wanning Sun
getTitle得到时间、标题及题评，并判断标题中是否有关键词，getContent得到内容
输入：财新网网页链接，输出网页内容
"""

import urllib2
import re

class Getnews:
    def __init__(self,baseUrl):
        self.baseUrl = baseUrl
        self.related = False
        
    # 传入页码，获取网页源代码
    def getPage(self):
        try:
            url = self.baseUrl
            print url
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read()
        except Exception,e:# 处理异常
            print e
            
    # 获取标题
    def getTitle(self):
        html = self.getPage()
        #print html

        re_title = re.compile(r'<div id="conTit">.*?<h1>(.*?)</h1>.*?id="pubtime_baidu">(.*?)</span>',re.S)
        title = re.findall(re_title,html)
        print title[0][0]
        if "招商银行" in title[0][0]  or "招商" in title[0][0] or "招行" in title[0][0]:
            self.related = True
            
            re_titlecomment = re.compile(r'<div id="subhead" class="subhead">(.*?)</div>',re.S)
            titlecomment = re.findall(re_titlecomment,html)
                    
            f = open('caixin.txt','a') 
            f.write('\n'+title[0][1]+'\t'+title[0][0]+'\t'+titlecomment[0].strip().replace('\n',' ')+'\t')
            f.close()
            
    # 获取正文
    def getContent(self):
        if self.related == False: return 
        
        html = self.getPage()

        re_content = re.compile(r'<div id="Main_Content_Val" class="text">(.*?)<a href=',re.S)
        content = re.findall(re_content,html)
        del_href = re.compile(r'<A href=".*?" target="_blank">',re.S)
        
        # 将正文写入文件
        for i in content:
            i = re.sub(del_href," ",i)
            i = i.replace('<P>','')
            i = i.replace('</P>','')
            i = i.replace('<B>','')
            i = i.replace('</B>','')
            i = i.replace('</A>','')
            i = re.sub(r'\s','',i)
        
            f = open('caixin.txt','a')# 此处是写入正文内容，所以用a
            f.write(i+' ')
            f.close()
            
#for i in open('url.txt'):

if __name__ == "__main__":    
    baseURL = 'http://www.baidu.com/link?url=OENaIA-pA6tsVIaASfgDytMyPbE9QXCagt0D19c77HAZNSPu_Kfalhm_3uOcXH45UjnXlJSjb9FpJBisIzMH0q'
    ls = Getnews(baseURL)
    print "爬虫已启动..."

    ls.getTitle()
    ls.getContent()
    print "正在抓取第%s页的内容" % (1)