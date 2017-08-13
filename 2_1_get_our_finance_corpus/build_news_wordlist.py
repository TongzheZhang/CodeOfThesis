# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 02:06:20 2016
构建财经新闻的词列表要求这个词出现三次以上，我们这里用的是五个公司的一年的新闻，可以根据新闻库的大小调节个数
时间约15mins
@author: Richard
"""

import sys
sys.path.append("../")
import jieba
import codecs
import os


jieba.load_userdict("corpus_for_finance.txt")
'''#测试载入自己词库的情况
jieba.load_userdict("testcorpus.txt")
words = jieba.cut('去你妹的石墨烯被收购收购被收购')
print (' '.join(words))
'''
#数据源目录(二级目录)
sourceDataDir='to_build_corpus'

#数据源文件列表
fileLists = []


            
def getSourceFileLists(sourceDataDir):  
    fileLists = []
    subDirList = os.listdir(sourceDataDir)
    for subDir in subDirList:
        print subDir

        fileList = [ sourceDataDir+'/'+subDir]
        fileLists += fileList  
    print fileLists
    return  fileLists   
fileLists = getSourceFileLists(sourceDataDir)
nf = open(r'E:\study\master of TJU\0Subject research\code\Important\get_features\wordlist_of_news.txt','a')
if 0 < len(fileLists): 

    punctuations = ['','\n','\t',',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%'] 
    
    for fileName in fileLists:
        print fileName

        hFile = None
        content = None
        try:
            hFile = codecs.open(fileName,'r')#打开文件
            content = hFile.readlines()#安行读入
            print '行数:',len(content)
        except Exception,e:
            print e
        finally:
            if hFile:
                hFile.close()#关闭文件
        
        if content:#如果有内容
            fileFenci = [ x for x in jieba.cut(' '.join(content))]# 把所有行连接在一起，再分词
            fileFenci2 = [word for word in fileFenci if not word in punctuations]  #去掉所有标点符号
            print len(fileFenci2),len(fileFenci)
            print '不重复的词共有：',len(set(fileFenci2))
            texts = [fileFenci2] #list外又加了一个list
            all_tokens = fileFenci2
            #print texts
            #all_tokens = sum(texts, [])
            #print all_tokens
            print 'begin counting'
            tokens = set(word for word in set(all_tokens) if all_tokens.count(word) >= 3 )
            for token in tokens:
                #print token.encode('utf-8','ignore')
                nf.write(token.encode('utf-8','ignore')+'\n')
            #print ' '.join(tokens)
            print len(tokens)
    nf.close()

print 'Build wordlist of news done'