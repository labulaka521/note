import multiprocessing
import os
import time
import random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end-start)))


if __name__ == '__main__':
    print('Parent process %s.'%os.getpid())
    p = multiprocessing.Pool(multiprocessing.cpu_count())
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done')
    p.close()
    p.join()
    print('All done')
#Parent process 57993.
#Waiting for all subprocesses done
#Run task 0 (57994)...
#Run task 1 (57995)...
##Run task 2 (57996)...
#Run task 3 (57997)...
#Task 1 runs 0.47 seconds.
#Run task 4 (57995)...
#Task 2 runs 1.39 seconds.
#Task 0 runs 2.16 seconds.
#Task 3 runs 2.85 seconds.
#Task 4 runs 2.55 seconds.
#All done
# pool为4 所以一次只可以执行4个进程，创建了4个进程所以在第一个进程执行完时，第5个进程才可以执行
## 对Pool对象调用join()方法会等待所有子进程执行完毕，调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process了。
#
##请注意输出的结果，task 0，1，2，3是立刻执行的，而task 4要等待前面某个task完成后才执行，这是因为Pool的默认大小在我的电脑上是4，因此，最多同时执行4个进程。这是Pool有意设计的限制，并不是操作系统的限制。如果改成：
