import time
import threading
class CountdownTask:
    def __init__(self):
        self._running = True

    def terminate(self):
        print('stopping')
        self._running = False

    def run(self, n):
        while self._running and n > 0:
            print('T-minus',n)
            n -= 1
            time.sleep(1)

c = CountdownTask()
t = threading.Thread(target=c.run, args=(10,))
t.start()
c.terminate()
c._running = True
c.terminate()
t.join(
