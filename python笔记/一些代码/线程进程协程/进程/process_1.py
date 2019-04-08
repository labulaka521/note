import multiprocessing
import time

def process(num):
    time.sleep(num)
    print('Process', num)

if __name__ == '__main__':
    for i in range(5):
        p = multiprocessing.Process(target=process, args=(i,))
        p.daemon = True
        p.start()
        p.join()      # 将所有的子进程执行完后在返回
    print('CPU number: {}'.format(multiprocessing.cpu_count()))
    for p in multiprocessing.active_children():
        print(f'Child process name: {p.name} id: {p.pid}')
    print('Process End')
