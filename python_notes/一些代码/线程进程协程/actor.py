from queue import Queue
from threading import Thread,Event
# actor 是用来解决并发和分布式计算问题的方法之一
# actor 就是一个并发执行的任务，他只是简单的对发送给它的消息进行处理，作为对这些消息的相应，actor会决定是否要对其他的actor发送进一步的消息。
# actor 任务之间的通信且异步的。
class ActorExit(Exception):
    pass


class Actor:
    def __init__(self):
        self._mailbox = Queue()
        self._teminated = Event()

    def send(self, msg):
        self._mailbox.put(msg)

    def recv(self):
        msg = self._mailbox.get()
        if msg is ActorExit:
            raise ActorExit()
        return msg
    
    def close(self):
        self.send(ActorExit)


    def start(self):
        t = Thread(target=self._bootstrap)
        t.daemon = True
        t.start()

    def _bootstrap(self):
        try:
            self.run()
        except ActorExit:
            pass
        finally:
            self._teminated.set()

    def join(self):
        self._teminated.wait()


    def run(self):
        while True:
            msg = self.recv()



class printActor(Actor):
    def run(self):
        while True:
            msg = self.recv()
            print('Got:', msg)



