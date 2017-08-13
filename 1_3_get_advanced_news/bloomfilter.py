# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 15:59:29 2017
@author: Wanning Sun

采用bloomfilter过滤内容相同的新闻，并分别写入文件
"""

import redis
from hashlib import md5

class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret

class BloomFilter(object):
    def __init__(self, host='localhost', port=6379, db=0, blockNum=1, key='bloomfilter'):
        """
        :param host: the host of Redis
        :param port: the port of Redis
        :param db: witch db in Redis
        :param blockNum: one blockNum for about 90,000,000; if you have more strings for filtering, increase it.
        :param key: the key's name in Redis
        """
        self.server = redis.Redis(host=host, port=port, db=db)
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))
    
    def isContains(self, str_input):
        if not str_input:
            return False
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        ret = True
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret
    
    def insert(self, str_input):
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)


if __name__ == '__main__':
    """ 第一次运行时会显示 not exists!，之后再运行会显示 exists! """
    bf = BloomFilter()
    f = open(r'E:\study\master of TJU\0Subject research\code\Important\1_3_get_advanced_news\all_news.txt')
    news_list = f.readlines()
    f.close()
    for news in news_list:
        news_split = news.strip().split('\t')
        news_outcome = ''
        for num in range(1,len(news_split)):
            news_outcome = news_outcome + news_split[num] + '\t'
        if bf.isContains(news_outcome):   # 判断字符串是否存在news_split[1]):
            print 'exists!'
            f = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\del_news_bf.txt','a') 
            f.write('\n'+news.strip())
            f.close()
        else:
            print 'not exists!'
            bf.insert(news_outcome)#news_split[1])
            f = open(r'E:\study\master of TJU\0Subject research\code\Important\0_1_special_data\news_result_bf.txt','a') 
            f.write('\n'+news.strip())
            f.close()
    