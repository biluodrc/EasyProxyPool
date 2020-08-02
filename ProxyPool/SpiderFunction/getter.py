# -*- coding = utf-8 -*-
# @time: 2020/7/25 10:30
# Author: Biluo
# @File: getter.py

from ProxyPool.crawler import Crawler
from ProxyPool.redisClient import RedisClient

Pool_UPPER_THRESHOLD = 10000

class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        """
        判断数据库内容数量超过阈值
        :return: （bool）
        """
        if self.redis.count() > 10000:
            return True
        else:
            return False

    def run(self):
        """
        运行爬虫程序
        """
        print('开始获取代理')
        if not self.is_over_threshold():
            for callback_label in range(self.crawler.__CrawlFuncCount__):
                callback = self.crawler.__CrawlFunc__[callback_label]
                proxies = self.crawler.get_proxies(callback)
                for proxy in proxies:
                    self.redis.add(proxy)
