# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 10:22:32 2016

@author: TongzheZhang
Onepage从新浪股吧的贴吧得到一页列表的阅读数，链接，题目，日期
输入：股票代码和页数，输出阅读数，链接，题目，日期
"""

#-*- coding:utf-8 -*-
import urllib
import urllib2
import re
from xinlang_guba_onepage_content import SinaTiezi

class OnePage:
    def __init__(self,i,sIdx):
        #
        self.baseurl = 'http://guba.sina.com.cn/?s=bar&name='+sIdx+'&type=0&page='+str(i)
        self.sIdx = sIdx
        #print self.baseurl
        
    def getPage(self):
        try:
            url = self.baseurl
            content = urllib2.urlopen(url).read().decode('gbk','ignore').encode('utf-8')
            return content
        except Exception,e:# 处理异常
            print e
        
    def getUrl(self):
        page = self.getPage()
        #page.replace('fred','red')
        removeFred = re.compile('<span class="fred">')
        page = re.sub(removeFred,'<span class="red">',page)
        #print page
    
        reg = re.compile(r'<td><span class="red">(\d*)</span></td>.*?<td><span class="red">(\d*)</span></td>.*?<td>.*?<a href="(.*?)" target="_blank" class=" linkblack f14">(.*?)</a>(.*?)</td>.*?<td>.*?<div class="author">.*?</div>.*?</td>.*?<td>(.*?)</td>' ,re.S)
        tiezi_list = re.findall(reg,page)
        print 'the page has:',len(tiezi_list)
        result_list = []
        for i in tiezi_list:
            if '精华' not in i[4]:
                result_list.append(i)
                #print 'i am in'
            #print i[3],i[4]#阅读量，点赞数，链接，题目，日期
        #for i in result_list:
        #    print i[0],i[1],i[2],i[3],i[5]#注意是第五个是日期
        return result_list
        
if __name__ == "__main__":


    n = 1
    for i in range(18,92):#输入！页数范围
        print i,'pages'
        mypage = OnePage(i,'sh600018')#输入！股票代码
        
        tiezi_list = mypage.getUrl()

        for i in tiezi_list:

            print 'No.',n
            n = n+1
        
            baseURL = 'http://guba.sina.com.cn/'+i[2]
        
            myTiezi = SinaTiezi(baseURL,i[5].replace('月','-').replace('日',''),i[0],i[1])
            myTiezi.getTitle()
            myTiezi.getContent()

