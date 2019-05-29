# Event和对象标记类似， 允许线程等待某个事件发生
# 初始状态时时间被设置为0 。如果没有被设置而线程正在等待该事件，那么线程就会被阻断,直到时间被设置为止
# 当有线程设置了这个事件时，这会唤醒所有正在等待该事件的线程。
from threading import Thread, Event
import time

def countdown(n, start_env):
    print('countdown starting')
    start_env.set()             # 线程设置了事件 ，然后会唤醒所有正在等待该事件的线程
    while n>0:
        print('T-minus', n)
        n -= 1
        time.sleep(1)

start_env = Event()

print('lauching countdown')
t = Thread(target=countdown, args=(10, start_env))
t.start()

# 在此阻塞 
start_env.wait()
print('countdown is running')
