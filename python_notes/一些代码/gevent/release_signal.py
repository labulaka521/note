from gevent import sleep
from gevent.pool import Pool
from gevent.lock import BoundedSemaphore


sem = BoundedSemaphore(5)

# 当信号量的范围为0时，会一直阻塞除非另一个已经获得信号量的greenlet做出释放
# 当信号量范围初始值为1时，函数只会一个一个执行，因为acquire会减小信号量的范围为0 所以只可以等到release函数执行后信号量+1后其他greenlet才可以执行
# Worker1 0 acquired semaphore
# Worker2 0 released semaphore
# Worker1 1 acquired semaphore
# Worker2 1 released semaphore
# Worker3 3 acquired semaphore
# Worker4 3 released semaphore
# Worker3 4 acquired semaphore
# Worker4 4 released semaphore
# Worker3 5 acquired semaphore
# Worker4 5 released semaphore
#  信号量设置为2时 
# Worker1 0 acquired semaphore
# Worker1 1 acquired semaphore
# Worker2 0 released semaphore
# Worker2 1 released semaphore
# Worker3 3 acquired semaphore
# Worker3 4 acquired semaphore
# Worker4 3 released semaphore
# Worker4 4 released semaphore
# Worker3 5 acquired semaphore
# Worker4 5 released semaphore
def worker1(n):
    # print(sem)
    sem.acquire()           # 当信号量为0后 会阻塞
    # print(sem)
    print(f'Worker1 {n} acquired semaphore')
    sleep(0)
    sem.release()
    # print(sem)          # 提供信号量+1
    print(f'Worker2 {n} released semaphore')
def worker2(n):
    with sem:
        print(f'Worker3 {n} acquired semaphore')
        sleep(0)
    print(f'Worker4 {n} released semaphore')

pool = Pool()
pool.map(worker1, range(2))
pool.map(worker2, range(3,6))


