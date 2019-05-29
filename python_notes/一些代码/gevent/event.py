import gevent
from gevent.event import Event

evt = Event()

def setter():
    '三秒后，唤醒所有正在等待的线程'
    print('A: hey wait for me, I have to do something')
    gevent.sleep(3)
    print('OK, I am done')
    evt.set()

def waiter():
    '3秒后将不阻塞'
    print('I will wait for you')
    evt.wait()  #阻塞
    print('It is about time')

def main():
    gevent.joinall([
        gevent.spawn(setter),
        gevent.spawn(waiter),
        gevent.spawn(waiter),
        gevent.spawn(waiter),
        gevent.spawn(waiter),
        gevent.spawn(waiter),
        gevent.spawn(waiter),
    ])
main()
