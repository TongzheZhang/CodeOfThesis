# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 15:58:37 2016
综合大财经词库和新闻的词列表，得到重合部分，即最终的我们的财经词库。
@author: Richard
"""

f1 = open(r'E:\study\master of TJU\0Subject research\code\Important\get_features\wordlist_of_news.txt','r')
f2 = open(r'E:\study\master of TJU\0Subject research\code\Important\get_features\corpus_for_finance.txt','r')
f3 = open(r'E:\study\master of TJU\0Subject research\code\Important\get_features\final_corpus.txt','w')

lines1 = f1.readlines()
lines2 = f2.readlines()

print len(lines1)
print len(lines2)

 
referwords = {}.fromkeys([ line.rstrip().decode('utf8') for line in lines2 ])

num = 0
for line1 in lines1:
    if line1.rstrip().decode('utf8') in referwords:
        num += 1
        print line1.rstrip().decode('utf8')
        f3.write(line1)
print num
f1.close()
f2.close()
f3.close()
