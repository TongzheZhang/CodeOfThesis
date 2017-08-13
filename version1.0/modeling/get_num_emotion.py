# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 01:09:44 2016
得到情感词的数字
正股票情绪，负股票情绪，情绪强度
@author: Richard
"""

import jieba
import math
print math.e
import scipy.io as sio 
print pow(math.e,4)
'''打开数据'''
jieba.load_userdict(r'all_emotion_words.txt')
f = open('data.txt')
data = f.readlines()
f.close()

corpus = {}.fromkeys([ line.rstrip().decode('utf8') for line in open('all_emotion_words.txt') ])
pos_corpus = {}.fromkeys([ line.rstrip().decode('utf8') for line in open('pos_corpus.txt') ])
neg_corpus = {}.fromkeys([ line.rstrip().decode('utf8') for line in open('neg_corpus.txt') ])

print u'宗旨' in corpus

print len(data)

all_date = []
for i in data:
    temp = i.split('\t')
    all_date.append(temp[0][5:])
    
t = open('test_tieba.txt')
tieba_data = t.readlines()
t.close()

num_pos = []
num_neg = []
num_total = []
for idx,i in enumerate(all_date):
    pos_num_temp = 0
    neg_num_temp = 0
    total_temp = 0
    for t in tieba_data:
        t_temp = t.split('\t')
        if i==t_temp[0]:
            t_sen = t_temp[3]+' '+t_temp[4]+' '+t_temp[5]
            t_jieba = jieba.cut(t_sen)
            for j in t_jieba:
                total_temp += 1
                if j in pos_corpus:
                    pos_num_temp += 1
                if j in neg_corpus:
                    neg_num_temp += 1
    num_pos.append(pos_num_temp)
    num_neg.append(neg_num_temp)
    num_total.append(float(total_temp))
final_pos = []
final_neg = []

for_con_tensor = []

#用了五天的情绪累加，但是前四天用了后面的四天
for idx,i in enumerate(num_pos):
    print idx
    final_pos.append((num_pos[idx]/num_total[idx])*pow(math.e,-idx/20)+(num_pos[idx-1]/num_total[idx-1])*pow(math.e,-(idx-1)/20)+(num_pos[idx-2]/num_total[idx-2])*pow(math.e,-(idx-2)/20)+(num_pos[idx-3]/num_total[idx-3])*pow(math.e,-(idx-3)/20)+(num_pos[idx-4]/num_total[idx-4])*pow(math.e,-(idx-4)/20))
for idx,i in enumerate(num_neg):
    print idx
    final_neg.append((num_neg[idx]/num_total[idx])*pow(math.e,-idx/20)+(num_neg[idx-1]/num_total[idx-1])*pow(math.e,-(idx-1)/20)+(num_neg[idx-2]/num_total[idx-2])*pow(math.e,-(idx-2)/20)+(num_neg[idx-3]/num_total[idx-3])*pow(math.e,-(idx-3)/20)+(num_neg[idx-4]/num_total[idx-4])*pow(math.e,-(idx-4)/20))
w = open('num_emotion.txt','w')
for i in range(0,len(num_pos)):
    w.write(str(final_pos[i])+' '+str(final_neg[i])+' '+str((10**(-2))*(final_pos[i]-final_neg[i])/(final_pos[i]+final_neg[i]))+'\n')
    temp = []
    temp.append(final_pos[i])
    temp.append(final_neg[i])
    temp.append((10**(-5))*(final_pos[i]-final_neg[i])/(final_pos[i]+final_neg[i]))
    for_con_tensor.append(temp)
w.close()
sio.savemat('emo_features.mat', {'emo_features': for_con_tensor})