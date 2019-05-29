import threading
from contextlib import contextmanager


_local = threading.local()

@contextmanager
def acquire(*locks):
    # 排序锁
    locks = sorted(locks, key=lambda x: id(x))


    # 确保以前获取的锁不被侵害
    acquired = getattr(_local,'acquired',[])
    if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
        raise RunTimeError('Lock Order Violation')


    # 获取所有的锁
    acquired.extend(locks)
    _local.acquired = acquired


    try:
        for lock in locks:
            lock.acquire()
        yield
    finally:
        # 从后往前开始释放锁
        for lock in reversed(locks):
            lock.release()
        del acquired[-len(locks)]


x_lock = threading.Lock()
y_lock = threading.Lock()
def thread_1():
    while True:
        with acquire(x_lock,y_lock):
            print('Thread-1')

def thread_2():
    while True:
        with acquire(y_lock,x_lock):
            print('Thread-2')

t1 = threading.Thread(target=thread_1)
#t1.daemon = True
t1.start()

t2 = threading.Thread(target=thread_2)
#t2.daemon = True
t2.start()
