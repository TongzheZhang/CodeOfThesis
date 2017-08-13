# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 17:00:52 2016

@author: syd
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 10:22:32 2016

@author: syd
Onepage从东方财富吧的贴吧得到一页列表的阅读数，链接，题目，日期
输入：股票代码和页数，输出阅读数，链接，题目，日期
"""

#-*- coding:utf-8 -*-
import urllib
import urllib2
import re
from dfcf_guba_onepage_content import Tiezi

class OnePage:
    def __init__(self,i,sIdx):
        self.baseurl = 'http://guba.eastmoney.com/list,'+str(sIdx)+ ',f_' +str(i) +'.html'
        self.sIdx = sIdx
        
    def getPage(self):
        try:
            url = self.baseurl
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read()
        except Exception,e:# 处理异常
            print e
        
    def getUrl(self):
        page = self.getPage()
        reg = re.compile(r'<span class="l1">(\d*)</span><span class="l2">(\d*)</span><span class="l3"><a href="(.*?)" title=".*?" >(.*?)</a></span><span class="l4">.*?<span class="l6">(.*?)</span>' ,re.S)
        tiezi_list = re.findall(reg,page)
        print 'the page has:',len(tiezi_list)
        #for i in tiezi_list:
            #print i[0],i[1],i[2],i[3],i[4]#阅读数，评论数，链接，标题，时间
        return tiezi_list
        
if __name__ == "__main__":


    n = 1
    for i in range(21,25):#输入！页数范围,修改页数
        print i,'pages'
        mypage = OnePage(i,600018)#输入！股票代码，修改代码
        tiezi_list = mypage.getUrl()

        for i in tiezi_list:

            print n
            n = n+1

            baseURL = 'http://guba.eastmoney.com'+i[2]

            myTiezi = Tiezi(baseURL,i[4],i[0],i[1])
            myTiezi.getTitle()
            myTiezi.getContent()