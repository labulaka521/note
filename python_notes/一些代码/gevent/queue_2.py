import gevent
from gevent.queue import Queue, Empty

tasks = Queue(maxsize=3)

def worker(n):
    try:
        while True:
            task = tasks.get(timeout=0)
            print('Worker %s got task %s' % (n, task))
            gevent.sleep(0)
    except Empty:
        print('Quitting time')

def boss():
    for i in range(10):
        tasks.put(i)
    print('Assigned all work in interation 1')
    
    for i in range(10,20):
        tasks.put(i)
    print('Assigend all work in interation 2')

gevent.joinall([
    gevent.spawn(boss),
    gevent.spawn(worker, 'steve'),
    gevent.spawn(worker, 'john'),
    gevent.spawn(worker, 'bob')
])

