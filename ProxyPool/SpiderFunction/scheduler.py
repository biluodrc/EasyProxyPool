# -*- coding = utf-8 -*-
# @time: 2020/7/25 11:03
# Author: Biluo
# @File: scheduler.py

import time

TESTER_CYCLE = 20
GETTER_CYCLE = 20
TESTER_ENABLED = True
GETTER_ENABLED = True
# API_ENABLED = True

from multiprocessing import Process
from ProxyPool.getter import Getter
from ProxyPool.tester import Tester
from ProxyPool.redisClient import RedisClient


class Scheduler():
    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
        测试代理是否可用
        :param cycle: 测试循环周期
        """
        tester = Tester()
        while True:
            print(' 测试器开始运行 ')
            tester.run()
            time.sleep(cycle)

    def schedule_getter(self, cycle=GETTER_CYCLE):
        """
        定时获取代理
        :param cycle: 获取代理循环周期
        """
        getter = Getter()
        while True:
            print(' 开始抓取代理 ')
            getter.run()
            time.sleep(cycle)

    # def schedule_api(self):
    #     app.run(API_HOST, API_PORT)

    def run(self):
        """
        代理池运行程序
        """
        print(' 代理池开始运行 ')
        if TESTER_ENABLED:
            tester_process = Process(target=self.schedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process = Process(target=self.schedule_getter)
            getter_process.start()

        # if API_ENABLED:
        #     api_process = Process(target=self.schedule_api)
        #     api_process.start()

def main():
    s = Scheduler()
    s.run()

if __name__ == '__main__':
    main()