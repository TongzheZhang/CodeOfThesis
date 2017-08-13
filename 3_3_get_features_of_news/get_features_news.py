# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:39:53 2017
得到新闻数据的特征
@author: Richard
"""
import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import scipy.io as sio
from sklearn.decomposition import PCA

def get_features_news_func():
    '''打开数据'''
    jieba.load_userdict(r'E:\study\master of TJU\0Subject research\code\Important\0_0_common_data\final_corpus.txt')
    f = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\newsdata.txt')
    news_list = f.readlines()
    f.close()

    '''读取日期列表'''
    t = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\datelist.txt')
    datelist = t.readlines()
    all_date = []
    for i in range(0,len(datelist)):
        all_date.append(datelist[i][5:].strip('\n'))
    
    '''得到分割点'''
    split_num = int(round(len(all_date)*0.8))

    corpus = {}.fromkeys([ line.rstrip().decode('utf8') for line in open(r'E:\study\master of TJU\0Subject research\code\Important\0_0_common_data\final_corpus.txt') ])
    '''！！！构建新闻特征时应不应该加上情感词库'''
    #pos_corpus = {}.fromkeys([ line.rstrip().decode('utf8') for line in open('pos_corpus.txt') ])
    #neg_corpus = {}.fromkeys([ line.rstrip().decode('utf8') for line in open('neg_corpus.txt') ])


    '''处理文本'''
    X = []
    for i in news_list:
        l_one = jieba.cut(i)
        temp = []
        for t in l_one:       
            if t in corpus:
                temp.append(t)
        X.append(' '.join(temp))
    X_train = X[:split_num]
    X_test = X[split_num:] 

    '''计算特征'''
    basicvectorizer = CountVectorizer(ngram_range=(1,1))
    basictrain = basicvectorizer.fit_transform(X_train)
    transformer = TfidfTransformer()
    traintfidf = transformer.fit_transform(basictrain).toarray().tolist()#最后得到的训练集的特征

    basictest = basicvectorizer.transform(X_test)
    testtfidf = transformer.transform(basictest).toarray().tolist()#最后得到的测试集的特征

    print '特征维度：',len(traintfidf[0])

    '''PCA降维'''
    estimator = PCA(n_components=100)
    pca_X_train = estimator.fit_transform(traintfidf).tolist()
    pca_X_test = estimator.transform(testtfidf).tolist()
    '''得到合体的特征，并保存为mat文件'''
    totalftidf = traintfidf + testtfidf
    sio.savemat(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\news_features.mat', {'news_features': totalftidf})

    '''得到合体的特征，并保存为mat文件'''
    totalpca = pca_X_train+pca_X_test
    sio.savemat(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\news_features_pca.mat', {'news_features': totalpca})
    
if __name__ == "__main__":
    get_features_news_func()