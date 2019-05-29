from __future__ import print_function  # 必须放在首行，将python3的print函数引进python2.x
import gevent
from gevent import monkey
monkey.patch_all()

import time
import requests

urls = [
    'https://www.baidu.com',
    'https://www.apple.com',
    'https://www.python.org'
]
def print_head(url):
    print(f'Starting {url}')
    data = requests.get(url).text
    print(time.time())
    print(f'{url}: {len(data)} bytes')

jobs = [gevent.spawn(print_head, _url) for _url in urls]

gevent.wait(jobs)

