# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 16:04:34 2017
@author: Wanning Sun
getTitle得到时间及标题，并判断标题中是否有关键词，getContent得到内容
输入：人民网网页链接，输出网页内容
"""

import urllib2
import re

class Getnews:
    def __init__(self,baseUrl):
        self.baseUrl = baseUrl
        self.related = False
    def getPage(self):
        try:
            url = self.baseUrl
            content = urllib2.urlopen(url).read().decode('gbk','ignore').encode('utf-8')
            return content
        except Exception,e:# 处理异常
            print e
    """
    # 传入页码，获取网页源代码
    def getPage(self):
        try:
            url = self.baseUrl
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            html = response.read()
            type = sys.getfilesystemencoding()
            #utf-8为网页编码，可能为gbk等
            html = html.decode('utf-8').encode(type)
            return html
        except Exception,e:# 处理异常
            print e
    """     
    # 获取标题
    def getTitle(self):
        html = self.getPage()

        #print html
        
        re_title = re.compile(r'<div class="clearfix w1000_320 text_title">.*?<h1>(.*?)</h1>.*?<div class="fl">(.*?)&nbsp',re.S)
        title = re.findall(re_title,html)
        
        if "招商银行" in title[0][0]  or "招商" in title[0][0] or "招行" in title[0][0]:
            self.related = True
            f = open('people.txt','a') 
            f.write('\n'+title[0][1]+'\t'+title[0][0]+'\t')
            f.close()
    # 获取正文
    def getContent(self):
        if self.related == False: return 
        
        html = self.getPage()
        

        re_content = re.compile(r' <div class="fl text_con_left">(.*?)<div class="edit clearfix">',re.S)
        content = re.findall(re_content,html)
        del_href = re.compile(r'<(.*?)>',re.S)
        
        # 将正文写入文件
        for i in content:
            i = re.sub(del_href,"",i)
            i = re.sub(r'\s','',i)
        
            f = open('people.txt','a')# 此处是写入正文内容，所以用a
            f.write(i+' ')
            f.close()

        
if __name__ == "__main__":    
    baseURL = 'http://finance.people.com.cn/n1/2016/0915/c1004-28717763.html'
    ls = Getnews(baseURL)
    print "爬虫已启动..."

    ls.getTitle()
    ls.getContent()
    print "正在抓取第%s页的内容" % (1)
