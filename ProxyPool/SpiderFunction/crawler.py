# -*- coding = utf-8 -*-
# @time: 2020/7/24 23:15
# Author: Biluo
# @File: crawler.py

from pyquery import PyQuery as pq
import requests
import re

# 用于判断是否返回合法IP地址
pattern = re.compile('^((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}$')

def get_page(url , params=None):
    '''
    获取网页
    :param url: 目标网站
    :param params: get参数
    :return: 网页html
    '''
    return requests.get(url , params=params).text

class ProxyMetaclass(type):
    '''
    Crawler元类，用于获取需要执行的函数
    '''
    def __new__(cls , name , bases , attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k , v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls , name , bases , attrs)

class Crawler(object , metaclass=ProxyMetaclass):
    def get_proxies(self , callback):
        '''
        获取代理IP地址
        :param callback:
        :return: 代理IP地址（list）
        '''
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            print('成功获取到代理' , proxy)
            proxies.append(proxy)
        return proxies

    def crawl_89ip(self , page=10):
        """
        爬取89ip网站
        :param page: 页数
        """
        base_url = 'http://www.89ip.cn/index_'
        idx = 1
        while idx <= page:
            url = base_url + str(idx) + '.html'
            html = get_page(url)
            idx += 1
            doc = pq(html)
            items = doc.find('tr').items()
            for item in items:
                ip = item.find('td:nth-child(1)').text()
                port = item.find('td:nth-child(2)').text()
                if pattern.match(ip) == None:
                    continue
                yield ':'.join([ip , port])

    def crawl_jiangxianli(self , page = 10):
        """
        爬取jiangxiangli网站
        :param page: 页数
        """
        base_url = 'https://ip.jiangxianli.com/'
        params = {
            'page':1,
        }
        for i in range(1,page+1):
            params['page']=i
            html = get_page(base_url , params)
            doc = pq(html)
            items = doc.find('tr').items()
            for item in items:
                ip = item.find('td:nth-child(1)').text()
                port = item.find('td:nth-child(2)').text()
                if pattern.match(ip) == None:
                    continue
                yield ':'.join([ip , port])

    def crawl_66ip(self , page = 10):
        """
        爬取66ip网站
        :param page: 页数
        """
        base_url = 'http://www.66ip.cn/'
        for i in range(1,page+1):
            url = base_url+str(i)+'.html'
            html = get_page(url)
            doc = pq(html)
            items = doc.find('tr').items()
            for item in items:
                ip = item.find('td:nth-child(1)').text()
                port = item.find('td:nth-child(2)').text()
                if pattern.match(ip) == None:
                    continue
                yield ':'.join([ip , port])


# tem = Crawler()
# proxys = tem.crawl_66ip()
# for proxy in proxys:
#     print(proxy)