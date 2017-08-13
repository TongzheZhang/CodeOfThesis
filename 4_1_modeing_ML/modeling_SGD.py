# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 20:20:53 2016
对文本进行处理，对数据集进行分离，用各种机器学习模型建模
注意！python都是含左不含右
注意！删掉最后一个空行
最后得到一个预测的结果pred_result.txt
@author: Richard
"""
from sklearn.neighbors import KNeighborsRegressor
import scipy.io as sio 
'''读取日期列表'''
t = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\datelist.txt')
datelist = t.readlines()
date_list = []
for i in range(0,len(datelist)):
    date_list.append(datelist[i].strip('\n'))
total_len = len(date_list)
'''读入新闻特征'''
news_features_dict = sio.loadmat(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\news_features_pca')
news_list = news_features_dict['news_features'].tolist()
'''读入情感特征'''
emo_features_dict = sio.loadmat(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\emo_features')
emotion_list = emo_features_dict['emo_features'].tolist()
'''读入情感特征'''
firm_features_dict = sio.loadmat(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\firm_features')
firm_list = firm_features_dict['firm_features'].tolist()
'''读入y值'''
y_incre_dict = sio.loadmat(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\y_incre')
price_list = y_incre_dict['y_incre'].reshape(total_len).tolist()

#数据分割点  
split_num = int(round(len(date_list)*0.8))

print '分割点：',split_num
print '数据一共长：',len(date_list)


pca_X_train = news_list[:split_num]
pca_X_test = news_list[split_num:]

emotion_train = emotion_list[:split_num]
emotion_test = emotion_list[split_num:]

firm_train = firm_list[:split_num]
firm_test = firm_list[split_num:]

y_train = price_list[:split_num]
y_test = price_list[split_num:]

test_date_list = date_list[split_num:]


'''计算数据集的涨跌'''
di_real_train = []#train集涨跌的真实值，di代表direction
for i in y_train:
    if i >= 0:di_real_train.append(1)
    else:di_real_train.append(0)

di_real_test = []#test集涨跌的真实值
for i in y_test:
    if i >= 0:di_real_test.append(1)
    else:di_real_test.append(0)


'''加入情感词量，在降维后特征里'''
for idx,i in enumerate(pca_X_train):
    #加入情感特征
    pca_X_train[idx].append(float(emotion_train[idx][0]))
    pca_X_train[idx].append(float(emotion_train[idx][1]))
    pca_X_train[idx].append(float(emotion_train[idx][2]))
    pca_X_train[idx].append(float(emotion_train[idx][3]))
    pca_X_train[idx].append(float(emotion_train[idx][4]))
    pca_X_train[idx].append(float(emotion_train[idx][5]))
    #加入公司特征
    pca_X_train[idx].append(float(firm_train[idx][0]))
    pca_X_train[idx].append(float(firm_train[idx][1]))
    pca_X_train[idx].append(float(firm_train[idx][2]))   
    pca_X_train[idx].append(float(firm_train[idx][3]))
    pca_X_train[idx].append(float(firm_train[idx][4]))
    pca_X_train[idx].append(float(firm_train[idx][5]))   
for idx,i in enumerate(pca_X_test):
    #加入情感特征
    pca_X_test[idx].append(float(emotion_test[idx][0]))
    pca_X_test[idx].append(float(emotion_test[idx][1]))
    pca_X_test[idx].append(float(emotion_train[idx][2]))
    pca_X_test[idx].append(float(emotion_test[idx][3]))
    pca_X_test[idx].append(float(emotion_test[idx][4]))
    pca_X_test[idx].append(float(emotion_train[idx][5]))
    #加入公司特征
    pca_X_test[idx].append(float(firm_test[idx][0]))
    pca_X_test[idx].append(float(firm_test[idx][1]))
    pca_X_test[idx].append(float(firm_test[idx][2]))   
    pca_X_test[idx].append(float(firm_test[idx][3]))
    pca_X_test[idx].append(float(firm_test[idx][4]))
    pca_X_test[idx].append(float(firm_test[idx][5]))  
'''KNN回归'''
uni_knr=KNeighborsRegressor(weights='distance',n_neighbors = 3)#uniform平均回归，distance是根据距离加权回归
uni_knr.fit(pca_X_train,y_train)
uni_knr_y_pred = uni_knr.predict(pca_X_test)
print 'KNR的R方',uni_knr.score(pca_X_test,y_test)
di_pred_knr = []#预测回归二值化
for i in uni_knr_y_pred:
    if i >= 0:di_pred_knr.append(1)
    else:di_pred_knr.append(0)
#print 'KNR的报告：'
#print classification_report(di_pred_knr,di_real_test)

right_num = 0
for idx,i in enumerate(di_pred_knr):
    if di_pred_knr[idx] == di_real_test[idx]:
        right_num = right_num + 1
print '实际计算对的个数',right_num,float(right_num)/(total_len-split_num)

'''输出预测文本，哪里需要，把这段代码粘哪'''
f = open(r'E:\study\master of TJU\0Subject research\code\Important\5_1_mock_trading\pred_result.txt','w')
testlen = len(date_list)-split_num
for i in range(0,testlen):
    f.write(test_date_list[i]+'\t'+str(uni_knr_y_pred[i])+'\n')#修改预测名即可
f.close()
differ = y_test - uni_knr_y_pred
RMSE = sum([ i*i for i in differ])
print 'RMSE',RMSE