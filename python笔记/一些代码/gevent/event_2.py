import gevent
from gevent.event import AsyncResult
a = AsyncResult()

def setter():
    gevent.sleep(3) # 程序执行会转向waiter
    print('1')
    a.set('Hello')

def waiter(): 
    print(a.get())

gevent.joinall([
    gevent.spawn(setter),
    gevent.spawn(waiter),
])
