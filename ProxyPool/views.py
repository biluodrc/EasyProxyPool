# -*- coding = utf-8 -*-
# @time: 2020/8/2 21:27
# Author: Biluo
# @File: views.py

from django.http import HttpResponse
from .SpiderFunction.redisClient import RedisClient

def index(request):
    return HttpResponse('Welcome To BILUO ProxyPool')

def random(request):
    db = RedisClient()
    return HttpResponse(db.get_proxy())