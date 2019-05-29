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
        raise RuntimeError('Lock Order Violation')


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

def philosopher(left,right):
    while True:
        with acquire(left, right):
            print(threading.currentThread(),'eating')

nsticks = 5
chopsticks = [ threading.Lock() for n in range(nsticks) ]
for n in range(nsticks):
    t = threading.Thread(target=philosopher, args=(chopsticks[n],chopsticks[(n+1) % nsticks]))
    t.start()

