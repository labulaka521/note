from collections import deque
import time

def countdown(n):
    while n > 0:
        print('T-minus',n,time.time())
        yield
        n -= 1
    print('Blastoff!!')

def countup(n):
    x = 0
    while x < n:
        print('Count up', x,time.time())
        yield 
        x += 1


class TaskScheduler:
    def __init__(self):
        self._task_queue = deque()

    def new_task(self, task):
        self._task_queue.append(task)

    def run(self):
        while self._task_queue:
            task = self._task_queue.popleft()
            try:
                next(task)
                self._task_queue.append(task)
            except StopIteration:
                pass
            print(self._task_queue)




s = TaskScheduler()
s.new_task(countdown(5))
s.new_task(countup(5))
s.run()




