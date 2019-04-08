from threading import Thread, Event
import time


def countdown(n, started_evt):
    while n > 0:
        print('T-minus',n)
        n -= 1
        time.sleep(1)
    print('countdown starting')
    started_evt.set()


started_evt = Event()

t = Thread(target=countdown, args=(10,started_evt))
t.start()


started_evt.wait()

print('countdown is running')




