# 如果一个线程要不停的重复使用event对象，你最好使用Condition来代替
# 下面的代码使用Condition对象实现了一个周期定时器每当定时器超时的时候，其他线程都可以检测到

import threading
import time



class PeriodicTimer:
    def __init__(self, interval):
        self._interval = interval
        self._flag = 0
        self._cv = threading.Condition()

    def start(self):
        t = threading.Thread(target=self.run)
        t.daemon = True
        t.start()


    def run(self):
        while True:
            time.sleep(self._interval)
            while self._cv:
                self._flag ^= 1
                self._cv.notify_all()


    def wait_for_tick(self):
        with self._cv:
            last_flag = self._flag
            while last_flag == self._flag:
                self._cv.wait()


ptimer = PeriodicTimer(5)
ptimer.start()


def countdown(nticks):
    while nticks > 0:
        ptimer.wait_for_tick()
        print('T-minus',nticks)
        nticks -= 1

def countup(last):
    n = 0
    while n < last:
        ptimer.wait_for_tick()
        print('Counting', n)
        n += 1


threading.Thread(target=countdown,args=(10,)).start()
threading.Thread(target=countup,args=(5,)).start()



