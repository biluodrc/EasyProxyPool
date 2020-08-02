# -*- coding = utf-8 -*-
# @time: 2020/8/2 21:45
# Author: Biluo
# @File: get_proxy.py

import requests

PROXY_POOL_URL = 'http://localhost:8000/random'

def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
