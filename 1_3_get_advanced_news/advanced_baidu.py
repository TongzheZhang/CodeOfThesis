# -*- coding: utf-8 -*-
"""
Created on Mar 3 ,2017
@author: Wanning Sun
Onepage从百度高级搜索的页面得到各个搜索条目的题目、链接
输入：搜索结果首页链接及总页数，输出各条目链接
"""

import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from advanced_baidu_caixin import Getnews

class OnePage:
    def __init__(self,page_url,times):
        self.baseurl = page_url
        self.times = times  #需要获取页面总数
 
    #翻页
    def nextPage(self, driver):
        #每次点击next之后停顿5秒钟
        n_class = driver.find_elements_by_class_name('n')
        if len(n_class)!=0:
            next = n_class[len(n_class)-1]
        else:
            return
        next.click()
        time.sleep(5)
    
    #返回网页中所有条目（t），默认十条
    def getItems(self):
        try:
            sourcePage = driver.page_source
            soup = BeautifulSoup(sourcePage, "lxml")
            items = soup.find_all(class_ = "t")
        except Exception,e:# 处理异常
            print e
        return items
    
    #每个条目中找到超链接和名字
    def getContent(self):
        driver.get(self.baseurl)
        reg = re.compile(r'<h3 class="t"><a data-click=.*?href="(.*?)" target="_blank">(.*?)</a></h3>' ,re.S)
        for page_num in range(self.times):
            print "百度新闻列表第"+str(page_num+1)+"页"
            items = self.getItems()
            page = []
            print len(items)
            for i in range(len(items)):
                page = re.findall(reg,str(items[i]))
                print i+1
                #if "em" in temp[0][1]:   #判断搜索结果题目中是否有关键词
                try:
                    print page[0][0]
                    myNews = Getnews(page[0][0])
                    myNews.getTitle()
                    myNews.getContent()
                except:
                    print '搜索结果不标准'
            self.nextPage(driver=driver)
        
if __name__ == "__main__":
    #输入高级搜索首页链接
    base_url = "https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=2&tn=baiduhome_pg&wd=%E6%8B%9B%E5%95%86%E9%93%B6%E8%A1%8C&ct=2097152&si=finance.caixin.com&oq=%E6%8B%9B%E5%95%86%E9%93%B6%E8%A1%8C&rsv_pq=af51973000007222&rsv_t=6d2fMHktiXTIkANhVagWucGBMYVEZSHB2F9O7dYEWGXbcDI3VPP6iZrfbFA74D62SBp2&rqlang=cn&rsv_enter=1&gpc=stf%3D1451577600%2C1483199999%7Cstftype%3D2"
    #输入高级搜索总页数
    allpages = 1#76#
    driver = webdriver.Chrome()
    
    mypage = OnePage(base_url,allpages)
    mypage.getContent()
    
    driver.quit()
