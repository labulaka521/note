import time
from threading import Thread

def check():
    if t.is_alive():
        print("still running")
    else:
        print("Finished")
def countdown(n):
    while n > 0:
        print('T-minus', n)
        n -= 1
        time.sleep(2)
        check()


t = Thread(target=countdown,args=(10,),daemon=True)
t.start()

check()
