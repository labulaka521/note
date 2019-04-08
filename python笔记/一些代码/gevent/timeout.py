import gevent
from gevent import Timeout

second = 10

timeout = Timeout(6)
timeout.start()

def wait():
    gevent.sleep(5)

try:
    gevent.spawn(wait).join()
except Timeout:
    print('Could not complete')


# 使用上下文管理器  
time_to_wait = 5
class TooLong(Exception):
    pass

with Timeout(time_to_wait, TooLong):
    gevent.sleep(10)



#  对于各种Greenlet和数据结构相关的调用，gevent也提供了超时参数。
def wait():
    gevent.sleep(2)


#1
timer = Timeout(1).start()

thread1 = gevent.spawn(wait)

try:
    thread1.join(timeout=timer)
except Timeout:
    print('Thread 1 timed out')

timer = Timeout.start_new(1)
thread2 = gevent.spawn(wait)


#2
try:
    thread2.get(timeout=timer)
except:
    print('Thread 2 timed out')

#3
try:
    gevent.with_timeout(1, wait)
except Timeout:
    print('Thread 3 Time out')
