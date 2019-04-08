from queue import Queue
from threading import Thread


_sentunel = object()
def oroducer(out_q):
    while True:
        out_q.put(data)

    out_q.put(_sentinel)



def consumer(in_q):
    while True:
        data = in_q.get()

        if  data is _sentinel:
            break

