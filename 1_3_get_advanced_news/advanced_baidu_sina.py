# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 19:34:24 2017
@author: Wanning Sun
getTitle得到时间及标题，并判断标题中是否有关键词，getContent得到内容
输入：新浪网网页链接，输出网页内容
"""

import urllib2
import re
import sys
import zlib
import socket
class Getnews:
    def __init__(self,baseUrl):
        self.baseUrl = baseUrl
        self.related = False
        
    def getPage(self):
        try:
            refer=None
            req = urllib2.Request(self.baseUrl)
            req.add_header('Accept-encoding', 'gzip')#默认以gzip压缩的方式得到网页内容
            if not (refer is None):
                req.add_header('Referer', refer)
            response = urllib2.urlopen(req, timeout=120)
            html = response.read()
            gzipped = response.headers.get('Content-Encoding')#查看是否服务器是否支持gzip
            if gzipped:
                html = zlib.decompress(html, 16+zlib.MAX_WBITS)#解压缩，得到网页源码
            return html
        except urllib2.HTTPError, e:
            return e.read()
        except socket.timeout, e:
            return ''
        except socket.error, e:
            return ''
    """
    # 传入页码，获取网页源代码
    def getPage(self):
        try:
            url = self.baseUrl
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            html = response.read()
            type = sys.getfilesystemencoding()
            html = html.decode('utf-8').encode(type)
            return html
        except Exception,e:# 处理异常
            print e
    """
    # 获取标题
    def getTitle(self):
        html = self.getPage()
        #print 'html',html
        
        re_title = re.compile(r'<div class="page-header">.*?">(.*?)</h1>',re.S)
        title = re.findall(re_title,html)
        re_time = re.compile(r'<meta name="weibo: article:create_at" content="(.*?)" />',re.S)
        time = re.findall(re_time,html)
        
        if len(title)==0 or len(time)==0:
            print 'len title = 0'
            return
      
        if "招商银行" in title[0]  or "招商" in title[0] or "招行" in title[0]:
            self.related = True
    
            f = open('sina.txt','a') 
            f.write('\n'+time[0]+'\t'+title[0]+'\t')
            f.close()
    # 获取正文
    def getContent(self):
        if self.related == False: return 
        
        html = self.getPage()

        re_content = re.compile(r'<div class="article article_16" id="artibody">.*?<!-- 原始正文start -->(.*?)<!-- 原始正文end -->',re.S)
        content = re.findall(re_content,html)
        del_href = re.compile(r'<(.*?)>',re.S)
        # 将正文写入文件
        for i in content:
            i = re.sub(del_href,"",i)
            i = re.sub(r'\s','',i)
        
            f = open('sina.txt','a')# 此处是写入正文内容，所以用a
            f.write(i+' ')
            f.close()
            

if __name__ == "__main__":    
    baseURL = 'http://finance.sina.com.cn/money/bond/20161122/100025502929.shtml'
    #ls = Getnews(baseURL)

    print "爬虫已启动..."
    ls = Getnews(baseURL)
    ls.getTitle()
    ls.getContent()
    print "正在抓取第%s页的内容" % (1)