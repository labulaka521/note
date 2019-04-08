# 信号量 Semaphore 
# 互斥锁，同时只允许一个进程更改数据
# Semaphore 信号量是同时允许一定数量的线程更改数据
# 


from multiprocessing import Process, Semaphore
import time
import random


def run(sem, user):
    sem.acquire()
    print('%s 进程' % user)
    time.sleep(random.randint(0, 3)) 
    sem.release()


if __name__ == '__main__':
    sem = Semaphore(3)          # 设置信号量为3 当信号量的值大于3时则后续的进程需要等待，加锁时信号量的计数+1 释放锁时，信号量的技术-1
    p_l = []
    for i in range(10):
        p = Process(target=run, args=(sem, 'user%s' % i,))
        p.start()
        p_l.append(p)

    for i in p_l:
        i.join()
    print('============》')

