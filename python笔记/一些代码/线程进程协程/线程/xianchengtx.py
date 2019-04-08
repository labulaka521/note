# 线程间通信
from queue import Queue
from threading import Thread, Event

def producer(out_q):
    n = 1
    while n <10:
        print('run producer')
        out_q.put('producer data')
        n += 1


def consumer(in_q):
    while True:
        data = in_q.get()
        print(data)
        in_q.task_done()

q = Queue()
t1 = Thread(target=consumer, args=(q,))
t2 = Thread(target=producer, args=(q,))

t1.start()
t2.start()

q.join()


# 当消费者已经处理了某项数据后，生产者需要对此立即感知的话 就需要将发送的数据和一个Event对象陪在一起

