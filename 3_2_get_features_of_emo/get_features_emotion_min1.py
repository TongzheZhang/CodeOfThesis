# -*- coding: utf-8 -*-
"""
Created on Tue Dec 27 01:09:44 2016
得到情感词的数字
正股票情绪，负股票情绪，情绪强度
附加到min1上
@author: Richard
"""

import jieba
import math
print math.e
import scipy.io as sio 
print pow(math.e,4)
'''读取日期列表'''
t = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\date_list_min1.txt')
datelist = t.readlines()
all_date = []
#去除年份
for i in range(0,len(datelist)):
    all_date.append(datelist[i][5:10].strip('\n'))

'''载入词库'''
jieba.load_userdict(r'E:\study\master of TJU\0Subject research\code\Important\0_0_common_data\all_emotion_words.txt')
corpus = {}.fromkeys([ line.rstrip().decode('utf8') for line in open(r'E:\study\master of TJU\0Subject research\code\Important\0_0_common_data\all_emotion_words.txt') ])
pos_corpus = {}.fromkeys([ line.rstrip().decode('utf8') for line in open(r'E:\study\master of TJU\0Subject research\code\Important\0_0_common_data\pos_corpus.txt') ])
neg_corpus = {}.fromkeys([ line.rstrip().decode('utf8') for line in open(r'E:\study\master of TJU\0Subject research\code\Important\0_0_common_data\neg_corpus.txt') ])
print u'宗旨' in corpus

'''打开贴吧数据'''
t = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\test_tieba.txt')
tieba_data = t.readlines()
t.close()


'''通过公式计算贴吧情绪'''
num_pos = []
num_neg = []
num_total = []
for idx,i in enumerate(all_date):
    print idx
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
#为了防止没有帖子的问题，假设没有帖子时，情绪和前一天一样
for idx,i in enumerate(num_total):
    if i == 0:
        num_total[idx] = num_total[idx-1]
        num_pos[idx] = num_pos[idx-1]
        num_neg[idx] = num_neg[idx-1]
final_pos = []
final_neg = []
for_con_tensor = []
#用了五天的情绪累加，但是前四天用了后面的四天
for idx,i in enumerate(num_pos):
    final_pos.append((num_pos[idx]/num_total[idx])*pow(math.e,-idx/20)+(num_pos[idx-1]/num_total[idx-1])*pow(math.e,-(idx-1)/20)+(num_pos[idx-2]/num_total[idx-2])*pow(math.e,-(idx-2)/20)+(num_pos[idx-3]/num_total[idx-3])*pow(math.e,-(idx-3)/20)+(num_pos[idx-4]/num_total[idx-4])*pow(math.e,-(idx-4)/20))
for idx,i in enumerate(num_neg):
    final_neg.append((num_neg[idx]/num_total[idx])*pow(math.e,-idx/20)+(num_neg[idx-1]/num_total[idx-1])*pow(math.e,-(idx-1)/20)+(num_neg[idx-2]/num_total[idx-2])*pow(math.e,-(idx-2)/20)+(num_neg[idx-3]/num_total[idx-3])*pow(math.e,-(idx-3)/20)+(num_neg[idx-4]/num_total[idx-4])*pow(math.e,-(idx-4)/20))

'''打开市场所有贴吧数据'''
m = open(r'E:\study\master of TJU\0Subject research\code\Important\0_0_common_data\all_market_emo.txt')
market_data = m.readlines()
m.close()
'''通过公式计算市场情绪'''
num_pos_m = []
num_neg_m = []
num_total_m = []
for idx,i in enumerate(all_date):
    print idx
    pos_num_temp = 0
    neg_num_temp = 0
    total_temp = 0
    for m in market_data:
        m_temp = m.split('\t')
        if i==m_temp[0]:
            m_sen = m_temp[3]+' '+m_temp[4]+' '+m_temp[5]
            m_jieba = jieba.cut(m_sen)
            for j in m_jieba:
                total_temp += 1
                if j in pos_corpus:
                    pos_num_temp += 1
                if j in neg_corpus:
                    neg_num_temp += 1
    num_pos_m.append(pos_num_temp)
    num_neg_m.append(neg_num_temp)
    num_total_m.append(float(total_temp))
#为了防止没有帖子的问题，假设没有帖子时，情绪和前一天一样
for idx,i in enumerate(num_total_m):
    if i == 0:
        num_total_m[idx] = num_total_m[idx-1]
        num_pos_m[idx] = num_pos_m[idx-1]
        num_neg_m[idx] = num_neg_m[idx-1]
final_pos_m = []
final_neg_m = []
#用了五天的情绪累加，但是前四天用了后面的四天
for idx,i in enumerate(num_pos_m):
    final_pos_m.append((num_pos_m[idx]/num_total_m[idx])*pow(math.e,-idx/20)+(num_pos_m[idx-1]/num_total_m[idx-1])*pow(math.e,-(idx-1)/20)+(num_pos_m[idx-2]/num_total_m[idx-2])*pow(math.e,-(idx-2)/20)+(num_pos_m[idx-3]/num_total_m[idx-3])*pow(math.e,-(idx-3)/20)+(num_pos_m[idx-4]/num_total_m[idx-4])*pow(math.e,-(idx-4)/20))
for idx,i in enumerate(num_neg):
    final_neg_m.append((num_neg_m[idx]/num_total_m[idx])*pow(math.e,-idx/20)+(num_neg_m[idx-1]/num_total_m[idx-1])*pow(math.e,-(idx-1)/20)+(num_neg_m[idx-2]/num_total_m[idx-2])*pow(math.e,-(idx-2)/20)+(num_neg_m[idx-3]/num_total_m[idx-3])*pow(math.e,-(idx-3)/20)+(num_neg_m[idx-4]/num_total_m[idx-4])*pow(math.e,-(idx-4)/20))   
#通过指数调节情绪强度特征的大小    
for i in range(0,len(num_pos)):
    temp = []
    temp.append(final_pos[i])
    temp.append(final_neg[i])
    temp.append((10**(-6))*(final_pos[i]-final_neg[i])/(final_pos[i]+final_neg[i]))
    temp.append(final_pos_m[i])
    temp.append(final_neg_m[i])
    temp.append((10**(-6))*(final_pos_m[i]-final_neg_m[i])/(final_pos_m[i]+final_neg_m[i]))
    for_con_tensor.append(temp)

sio.savemat(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\emo_features_min1.mat', {'emo_features': for_con_tensor})