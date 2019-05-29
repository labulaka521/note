import asyncio
import time

async def say_after(delay, what):
    
    await asyncio.sleep(1)
    print(delay)
    print(what)
    return what


# 并行执行
async def main():
    print(f"started at {time.strftime('%X')}")
    await say_after(1, 'hello')
    await say_after(2, 'word')

    print(f"finished at {time.strftime('%X')}")


# use asyncio.create_task函数并发运行作为asyncio任务的多个协程
async def main_multi():
    # task1 = asyncio.create_task(
    #     say_after(1, 'hello')
    # )
    # task2 = asyncio.create_task(
    #     say_after(2, 'word')
    # )
    # print(f"started at {time.strftime('%X')}")
    # await task1
    # await task2
    print(f"started at {time.strftime('%X')}")
    
    task = []
    for i in range(5):
        task.append(asyncio.create_task(
            say_after(i, 'test'+str(i))
        ))

    # print(task[0])
    # await task[0]
    for t in task:
        await task[i]
        print(task[i].result())

    print(f"finished at {time.strftime('%X')}")


# asyncio.run(main_multi(), debug=True)
# loop = asyncio.get


def now(): return time.time()


async def do_some_work(x):
    print('Waiting: ', x)
    return x

start = now()

coroutine = do_some_work(2)     # 返回一个生成器

loop = asyncio.get_event_loop()
# loop.run_until_complete(coroutine)

# print('TIME: ', now() - start)

# task = loop.create_task(coroutine)
task = loop.create_task(coroutine)
print(task)

loop.run_until_complete(task)
print(task.result())

# <Task pending coro=<do_some_work() running at /Users/admin/Desktop/Dropbox/笔记文件夹/日常笔记/一些代码/线程进程协程/协程/async2.py:56>>
# Waiting:  2
# <Task finished coro=<do_some_work() done, defined at /Users/admin/Desktop/Dropbox/笔记文件夹/日常笔记/一些代码/线程进程协程/协程/async2.py:56> result=2>


