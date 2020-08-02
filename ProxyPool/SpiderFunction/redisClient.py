# -*- coding = utf-8 -*-
# @time: 2020/7/24 23:30
# Author: Biluo
# @File: redisClient.py

import redis
from random import choice

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'ProxyPool'
INITIAL_SCORE = 10
MAX_SCORE = 100
MIN_SCORE = 0


class RedisClient(object):
    def __init__(self , host=REDIS_HOST , port=REDIS_PORT , pwd=REDIS_PASSWORD):
        self.db = redis.StrictRedis(host=host, port=port, password=pwd, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加一项ip为proxy，分数默认为INITIAL_SCORE的代理
        :param proxy: 代理ip
        :param score: 对应分数，默认INITIAL_SCORE
        :return: 返回添加的数据项
        """
        if not self.db.zscore(REDIS_KEY, proxy):
            return self.db.zadd(REDIS_KEY,{proxy:score})

    def get_proxy(self):
        """
        随机获得一个代理ip
        :return: 代理ip
        """
        results = self.db.zrangebyscore(REDIS_KEY , MAX_SCORE , MAX_SCORE)
        if results != None:
            return choice(results)
        else:
            results = self.db.zrevrange(REDIS_KEY , 0 , 100)
            if results != None:
                return choice(results)
            else:
                print('There is no legal proxy exits')

    def decrease(self , proxy):
        """
        将proxy对应的项分数减一，如分数到MIN_SCORE，则删除这一项
        :param proxy: 代理ip
        :return: 减小或删除的数据项
        """
        score = self.db.zscore(REDIS_KEY , proxy)
        if score > MIN_SCORE:
            print(' 代理 ', proxy, ' 当前分数 ', score, ' 减 1')
            return self.db.zincrby(REDIS_KEY , -1 , proxy)
        else:
            print(' 代理 ', proxy, ' 当前分数 ', score, ' 移除 ')
            return self.db.zrem(REDIS_KEY , proxy)

    def count(self):
        """
        返回数据库的大小
        :return: 数据库的大小
        """
        return self.db.zcard(REDIS_KEY)

    def max(self, proxy):
        """
        将proxy设置为MAX_SCORE
        :param proxy: 代理ip
        :return: 添加的proxy内容
        """
        print(' 代理 ', proxy, ' 可用，设置为 ', MAX_SCORE)
        return self.db.zadd(REDIS_KEY, {proxy:MAX_SCORE})

    def exits(self , proxy):
        """
        判断proxy是否存在于数据库中
        :param proxy: 代理ip
        :return: bool 是否存在于数据库中
        """
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def all(self):
        """
        返回数据库中所有的代理
        :return: 数据库中所有的代理
        """
        return self.db.zrangebyscore(REDIS_KEY , MIN_SCORE , MAX_SCORE)
