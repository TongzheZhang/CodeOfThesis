# -*- coding: utf-8 -*-
"""
Created on Mon jDec 19 20:20:53 2016
用滚动的方法，即过了一天便有了一天的经验
@author: Richard
"""
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeRegressor,DecisionTreeClassifier
import random
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.decomposition import PCA
import numpy as np
'''打开数据'''
jieba.load_userdict(r'final_corpus.txt')
f = open('data.txt')
data = f.readlines()
f.close()

price_list = []
news_list = []
date_list = []
for temp in data:
    newdata = temp.split('\t')
    price_list.append(float(newdata[1]))
    news_list.append(newdata[2])
    date_list.append(newdata[0])
#数据分割点  
split_num = int(round(len(news_list)*0.8))

print split_num

y_train = price_list[0:split_num]
y_test = price_list[split_num:]
X = []
corpus = {}.fromkeys([ line.rstrip().decode('utf8') for line in open('final_corpus.txt') ])

#print corpus
'''处理文本'''
for i in news_list:
    l_one = jieba.cut(i)
    temp = []
    for t in l_one:       
        if t in corpus:
            temp.append(t)
    X.append(' '.join(temp))
X_train = X[0:split_num]
X_test = X[split_num:]           
test_date_list = date_list[split_num:]  
'''计算特征'''
basicvectorizer = CountVectorizer(ngram_range=(1,1))
basictrain = basicvectorizer.fit_transform(X_train)
transformer = TfidfTransformer()
traintfidf = transformer.fit_transform(basictrain).toarray()#最后得到的训练集的特征

basictest = basicvectorizer.transform(X_test)
testtfidf = transformer.transform(basictest).toarray()#最后得到的测试集的特征

print '第一个新闻的tfidf特征：',testtfidf[0]

'''计算数据集的涨跌'''
di_real_train = []#train集涨跌的真实值，di代表direction
for i in y_train:
    if i >= 0:di_real_train.append(1)
    else:di_real_train.append(0)
    
num_test_1 = 0   
di_real_test = []#test集涨跌的真实值
for i in y_test:
    if i >= 0:
        di_real_test.append(1)
        num_test_1 += 1 
    else:di_real_test.append(0)

di_real = []
for i in price_list:
    if i >= 0:di_real.append(1)
    else:di_real.append(0)

y_pred = []
'''回归解决问题'''
for i in range(0,len(di_real_test)):
    print i
    dtr = DecisionTreeRegressor()
    dtr.fit(traintfidf,y_train)
    y_pred.append(dtr.predict(testtfidf[i]))
    traintfidf = np.vstack((traintfidf, testtfidf[i]))#这样合并好么？
    y_train.append(y_test[i])
di_pred = []#预测回归二值化
for i in y_pred:
    if i >= 0:di_pred.append(1)
    else:di_pred.append(0)
print '回归树的报告：'
print classification_report(di_pred,di_real_test)

print y_pred

f = open('pred_result.txt','a')
testlen = len(date_list)-split_num
for i in range(0,testlen):
    f.write(test_date_list[i]+'\t'+str(y_pred[i][0])+'\n')
f.close()

'''随机的结果'''
ran_re = []
for i in range(0,44):
    ran_re.append(random.randint(0, 1))
print '随即猜的结果：'
print classification_report(ran_re,di_real_test)
print num_test_1

        