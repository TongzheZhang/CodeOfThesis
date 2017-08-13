# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 17:00:52 2016

@author: Tongzhe Zhang
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 10:22:32 2016

@author: Tongzhe Zhang
新浪股吧
"""

#-*- coding:utf-8 -*-
import urllib
import urllib2
import re


# 连接http://guba.eastmoney.com/list,600848_1.html

class SinaTiezi:
    def __init__(self,baseUrl,date,reading,commenting):
        self.baseUrl = baseUrl
        self.date = date
        self.reading = reading
        self.commenting = commenting

    # 传入页码，获取网页源代码
    def getPage(self):
        try:
            url = self.baseUrl
            content = urllib2.urlopen(url).read().decode('gbk','ignore').encode('utf-8')
            return content
        except Exception,e:# 处理异常
            print e
            
    # 获取标题和帖主内容
    def getTitle(self):
        #载入源代码
        html = self.getPage()
        print html
        #找到所有帖子题目和帖主内容
        reg = re.compile(r'<h4 class=.*?>(.*?)</h4>',re.S)#正则表达式中，“.”的作用是匹配除“\n”以外的任何字符
        titlecomment = re.compile(r'<div class=.ilt_p. id="thread_content">(.*?)</div>',re.S)
        items = re.findall(reg,html)#正则表达式 re findall 方法能够以列表的形式返回能匹配的子串。
        titlecomment = re.findall(titlecomment,html)
 
        #编译表情和待去除的标签
        emoji = re.compile(r'<span class="face-img .*?><span class="face-img .*?>\[(.*?)\]</span></span>',re.S)
        removeAddr = re.compile('<span class="face-img .*?</span></span>')#去除表情
        removeOther = re.compile('<.*?>')#去除所有连接        
        
        #找到所有的表情
        emintitle = re.findall(emoji,items[0])
        emincon = re.findall(emoji,titlecomment[0])
        #去除表情和所有标签
        titlecomment[0] = re.sub(removeAddr,"",titlecomment[0])
        titlecomment[0] = re.sub(removeOther,"",titlecomment[0])
        items[0] = re.sub(removeAddr,"",items[0])
        items[0] = re.sub(removeOther,"",items[0])

        #替换表情为文字
        for a in range(len(emintitle)):
            items[0] = emintitle[a] + ' '+ items[0]           
        for a in range(len(emincon)):
            titlecomment[0] = emincon[a] + ' '+ titlecomment[0]       
        #删除开头结尾的空格
        titlecomment[0] = titlecomment[0].strip().replace('\n',' ')        
        items[0] = items[0].strip()
        
        #print items[0]
        #print titlecomment[0]
        f = open('sina.txt','a') # 文件名最好是英文，中文识别不了
        f.write('\n'+self.date + '\t' +str(self.reading)+'\t'+str(self.commenting)+'\t'+ items[0]+'\t'+titlecomment[0] +'\t')
        f.close()
        
        #print items[0]
        #print titlecomment[0]
        return items

    # 获取正文
    def getContent(self):
        html = self.getPage()
        
        reg = re.compile(r'<p class=.ilt_p.*?>(.*?)</p>',re.S)
        req = re.findall(reg,html)
        
        emoji = re.compile(r'<span class="face-img .*?><span class="face-img .*?>\[(.*?)\]</span></span>',re.S)
        removeAddr = re.compile('<span class="face-img .*?</span></span>')#去除表情
        removeOther = re.compile('<.*?>')#去除所有连接
        


        for i in req:
                  
            em = re.findall(emoji,i)
            i = re.sub(removeAddr,"",i)
            i = re.sub(removeOther,"",i)
            for a in range(len(em)):
                i = em[a]+" "+i 
            #print i
            
            f = open('sina.txt','a')# 此处是写入正文内容，所以用a
            f.write(i+' ')
            f.close()
            
        


#daseURL = 'http://guba.eastmoney.com/news,600848,429878160.html'
if __name__ == "__main__":    
    baseURL = 'http://guba.sina.com.cn/?s=thread&tid=346370&bid=1560' 
    ls = SinaTiezi(baseURL,'11-11',1,1)
    print "爬虫已启动..."

    ls.getTitle()
    ls.getContent()
    print "正在抓取第1页的内容"