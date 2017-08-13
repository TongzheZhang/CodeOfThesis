# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 14:35:12 2016
通过搜集到的新闻库去构建新闻集合，用于语料库筛选
@author: Richard
"""
import sys
sys.path.append("../")
import os


#数据源目录(二级目录)
sourceDataDir='news'
def getSourceFileLists(sourceDataDir):  
    fileLists = []
    subDirList = os.listdir(sourceDataDir)

    for subDir in subDirList:
        print subDir

        fileList = [ sourceDataDir+'/'+subDir]
        fileLists += fileList  
    print fileLists
    return  fileLists   

    

    
if __name__ =='__main__':
    
    fileLists = getSourceFileLists(sourceDataDir)
    nf = open(r'E:\study\master of TJU\0Subject research\code\Important\get_features\to_build_corpus\refertext.txt','w')
    nf.write('start\n')
    for fileName in fileLists:
        print fileName
        f = open(fileName)
        lines = f.readlines()
        for line in lines:
            newline = line.split('\t')[3] +' ' + line.split('\t')[4]+'\n'
            nf.write(newline)

        f.close()
        
    nf.close()