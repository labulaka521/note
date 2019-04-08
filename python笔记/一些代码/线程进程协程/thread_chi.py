from queue import Queue
import  threading
import time
queue = Queue()

# 定义需要线程池执行的任务
status = list()
def do_job():
    while True:
        i = queue.get()
        time.sleep(1)
        print('index %s, curent: %s' % (i, threading.current_thread()))
        status.append(threading.current_thread())
        queue.task_done()
if __name__ == '__main__':
    # 创建包括3个线程的线程池
    for i in range(5):
        t = threading.Thread(target=do_job)
        t.daemon=True # 设置线程daemon  主线程退出，daemon线程也会推出，即时正在运行
        t.start()

    # 模拟创建线程池3秒后塞进10个任务到队列
    time.sleep(3)
    for i in range(10):
        queue.put(i)

    queue.join()
    # 会一直阻塞，直到队列中所有的message都被get出来并且调用task_done才会返回
    print(status)
