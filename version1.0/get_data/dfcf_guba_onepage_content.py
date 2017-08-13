# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 17:00:52 2016

@author: Tongzhe Zhang
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 10:22:32 2016

@author: Tongzhe Zhang
东方财富贴吧，得到
"""

#-*- coding:utf-8 -*-
import urllib
import urllib2
import re


# 连接http://guba.eastmoney.com/list,600848_1.html

class Tiezi:
    def __init__(self,baseUrl,date,reading,commenting):
        self.baseUrl = baseUrl
        self.date = date
        self.reading = reading
        self.commenting = commenting
        #self.seeLZ ='?see_lz=' + str(seeLZ)
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
        reg = re.compile(r'<div id="zwconttbt">(.*?)</div>',re.S)
        titlecomment = re.compile(r'<div class="stockcodec">(.*?)</div>',re.S)

        items = re.findall(reg,html)#正则表达式 re findall 方法能够以列表的形式返回能匹配的子串。
        if items!=[]:
            self.result = True

            titlecomment = re.findall(titlecomment,html)
            #print items# it is a list
            # 将标题写入文件
    
            
            #remove others
            emoji = re.compile(r'<img src.*? title="(.*?)"/>',re.S)
            em = re.findall(emoji,items[0])
            
            removeAddr = re.compile('<img src.*?/>')#去除表情
            removeBlank = re.compile('\s')
            removeAll = re.compile('<.*?>')
            items[0] = re.sub(removeAddr,"",items[0])
            items[0] = re.sub(removeBlank," ",items[0])
            items[0] = re.sub(removeAll," ",items[0])
            
            for a in range(len(em)):
                items[0] = items[0]+' '+em[a]
      
    
            emc = re.findall(emoji,titlecomment[0])
            
            titlecomment[0] = re.sub(removeAddr,"",titlecomment[0])
            titlecomment[0] = re.sub(removeBlank," ",titlecomment[0])
            titlecomment[0] = re.sub(removeAll," ",titlecomment[0])
            
            titlecomment[0] = titlecomment[0].strip()
            for a in range(len(emc)):
                titlecomment[0] = titlecomment[0]+' '+emc[a]      
            titlecomment[0] =titlecomment[0].replace("<br>"," ")
            items[0] = items[0].replace("<br>"," ")
            '''
            f = open('dfcf.txt','a') 
            f.write('\n'+self.date + '\t' +str(self.reading)+'\t'+str(self.commenting)+'\t'+ items[0].strip().replace('\n',' ')+'\t'+titlecomment[0].strip().replace('\n',' ') +'\t')
            f.close()
            '''
            if 'div' in titlecomment[0]:
                f = open('dfcf.txt','a') # 文件名最好是英文，中文识别不了
                f.write('\n'+'题评中有div，可能有特殊符号')
                f.close()
                self.title_result=False
            elif int(self.reading) < int(self.commenting) :
                f = open('dfcf.txt','a') # 文件名最好是英文，中文识别不了
                f.write('\n'+'发现问题：下一行的阅读数小于评论数？？')
                f.write('\n'+self.date + '\t' +str(self.reading)+'\t'+str(self.commenting)+'\t'+ items[0].strip().replace('\n',' ')+'\t'+titlecomment[0].strip().replace('\n',' ') +'\t')
                f.close()
            else:
                f = open('dfcf.txt','a') # 文件名最好是英文，中文识别不了
                f.write('\n'+self.date + '\t' +str(self.reading)+'\t'+str(self.commenting)+'\t'+ items[0].strip().replace('\n',' ')+'\t'+titlecomment[0].strip().replace('\n',' ') +'\t')
                f.close()
            
            #print items[0]
            #print titlecomment[0]
            return items
        else:
            self.result = False
            f = open('dfcf.txt','a') 
            f.write('\n'+'网页不规范，标题为空')
            f.close()

    # 获取正文
    def getContent(self):
        if self.result==False:
            return
            
        html = self.getPage()
        reg = re.compile(r'<div class="zwlitext stockcodec">(.*?)</div>',re.S)
        req = re.findall(reg,html)
        emoji = re.compile(r'<img src.*? title="(.*?)"/>',re.S)

        removeAddr = re.compile('<img src.*?/>')#去除表情
        removeBlank = re.compile('\s')
        removeLink = re.compile('<a href.*?</a>')#去除链接
        # 将正文写入文件
        for i in req:
            #removeAddr = re.compile('<a.*?</a>')#去除超链接
            #i = re.sub(removeAddr,"",i)# 找到并替换，比replace更强大
            

            em = re.findall(emoji,i)
            i = re.sub(removeAddr,"",i)
            i = re.sub(removeBlank," ",i)
            i = re.sub(removeLink,"",i)
            i = i.replace("<br>"," ")
            #print i
            for a in range(len(em)):
                i = i +" "+em[a]
            #print i
            
            f = open('dfcf.txt','a')# 此处是写入正文内容，所以用a
            f.write(i+' ')
            f.close()
            
        


#daseURL = 'http://guba.eastmoney.com/news,600848,429878160.html'
if __name__ == "__main__":    
    #baseURL = 'http://guba.eastmoney.com/' + str(raw_input(u'http://guba.eastmoney.com/')) 
    baseURL = 'http://guba.eastmoney.com/news,601857,545801513.html'
    ls = Tiezi(baseURL,'11-11',1,1)
    print "爬虫已启动..."

    ls.getTitle()
    ls.getContent()
    print "正在抓取第%s页的内容" % (1)