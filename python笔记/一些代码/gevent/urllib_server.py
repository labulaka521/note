from gevent import monkey
monkey.patch_socket()
import time
import gevent
import requests
import json

def fetch(pid):
    response = requests.get('http://httpbin.org/get')
    result = response.json()
    print(result,time.time())

    return result


def asynchronous():
    threads = []
    for i in range(10):
        threads.append(gevent.spawn(fetch, i))
    gevent.joinall(threads)

print('Asynconous')
asynchronous()

