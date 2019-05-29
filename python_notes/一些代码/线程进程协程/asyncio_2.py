import threading
import asyncio



@asyncio.coroutine
def hello1():
    print('Hello Word! {}'.format(threading.currentThread()))
    yield from asyncio.sleep(1)
    print('Hello again! {}'.format(threading.currentThread()))


loop = asyncio.get_event_loop()
tasks = [hello1(),hello1()]
loop.run_until_complete(asyncio.wait(tasks))
oop.close()
