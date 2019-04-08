import threading
import time


class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print("T-minus",n)
            n -= 1
            time.sleep(3)


c = CountdownTask()
t = threading.Thread(target=c.run,args=(10,))
t.start()
c.terminate()
t.join()
