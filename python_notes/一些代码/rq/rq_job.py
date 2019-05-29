'''
运行的函数不可以和rq任务队列放在一个文件执行
'''
import time
from job_main import add

job = add.delay(2,1)
print(job.result)
time.sleep(1)
print(job.result)
