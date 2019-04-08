import random

import gevent
import time

def task(pid):
    """
    Some non-deterministic task
    """
    gevent.sleep(random.randint(0, 2) * 0.001)
    print('Task %s done' % pid)


def synchronous():
    for i in range(1,10):
        task(i)


def asynchronous():
    threads = [gevent.spawn(task, i) for i in range(1, 10)]
    gevent.joinall(threads)

time1 = time.time()
print('Synchronous:',)
synchronous()
time2 = time.time()
print(time2-time1)

print('Asynchronous:')
asynchronous()
print(time.time()-time2)
