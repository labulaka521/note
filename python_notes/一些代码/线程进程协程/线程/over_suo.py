# 在多线程程序中出现死锁的常见原因就是线程一次尝试获取了多次锁。
# 如果有一个线程获取到第一个锁， 但是在尝试获取第二个锁时阻塞了，那么这个线程就有可能阻塞其他线程的执行，进而使得整个程序僵死


# 避免产生死锁的一种解决方案就是给程序中的每一个锁分配一个唯一的数字编号，并且在获取多个锁时指按照编号的升序方式来获取。
# 
# 避免死锁的基本原则是，只要保证线程一次只持有一把锁，那么程序就不会出现死锁
# 

import threading
from contextlib import contextmanager

_local = threading.local()


# 锁管理器
# 先将锁按照对象id排序，然后在程序会加锁，然后到yield等待调用后，然后逆序locks 锁，释放锁
@contextmanager
def acquire(*locks):
    locks = sorted(locks, key=lambda x: id(x))
    # 将锁按照对象ID排序

    acquired = getattr(_local, 'acquired', [])
    # print(acquired)
    if acquired and max(id(lock) for lock in acquired) > id(locks[0]):
        raise RuntimeError('Lock Order Violation')

    acquired.extend(locks)
    _local.acquired = acquired
    try:
        for lock in locks:
            lock.acquire()

        yield
    finally:
        for lock in reversed(locks):
            # 释放锁时需要按照逆序释放
            lock.release()
        del acquired[-len(locks):]



# x_lock = threading.Lock()
# y_lock = threading.Lock()

# def Thread_1():
#     while True:
#         with acquire(x_lock, y_lock):
#             print('Thread_1')


# t1 = threading.Thread(target=Thread_1)
# # t1.daemon = True
# t1.start()


# def Thread_2():
#     while True:
#         with acquire(y_lock, x_lock):
#             print('Thread_1')


# t2 = threading.Thread(target=Thread_2)
# # t1.daemon = True
# t2.start()


#  哲学家就餐问题

def philospher(left, right):
    while True:
        with acquire(left, right):
            print(threading.currentThread(), 'eating')

NSTICKS = 5
chopticks = [threading.Lock() for n in range(NSTICKS)]

for i in range(NSTICKS):
    t = threading.Thread(target=philospher, args=(chopticks[i], chopticks[(i+1) % NSTICKS]))
    t.start()
