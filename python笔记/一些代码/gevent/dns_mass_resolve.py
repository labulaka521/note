from __future__ import print_function
import gevent
from gevent import socket
from gevent.pool import Pool


N = 1000
pool = Pool(1000)
finished = 0

def job(url):
    global finished
    try:
        try:
            ip = socket.gethostbyname(url)
            print(f'{url}={ip}')
        except socket.gaierror as ex:
            print(f'{url} failed with with {ex}')
    finally:
        finished += 1
with gevent.Timeout(10, False):
    for x in range(10+N):
        pool.spawn(job, f'{x}.com')
    pool.join()


print(f'finished within 2 seconds: {finished}/{N}')

