'''
Note 运行的函数和rq进入队列的ip不能在同一文件中

Make sure that the function’s __module__ is importable by the worker. 
In particular, this means that you cannot enqueue functions that are declared in the __main__ module
'''
from rq import Queue
from redis import Redis
from count_words import count_words_at_url
import time



# Tell RQ what Redis connection to use
redis_conn = Redis()
# 放入名为low的队列 使用rq worker low启动  监听low这个队列
# no args implies the default queue
q = Queue('low',connection=redis_conn)
# is_async = False, 阻塞执行
# Delay execution of count_words_at_url('http://nvie.com')

job = q.enqueue(count_words_at_url, 'https://github.com', result_ttl=10)

# for i in q.jobs:
#     print(i.key)
print(job.result)   # => None
# Now, wait a while, until the worker is finished
time.sleep(2)
print(job.result)


# # print(q.name)
# # enqueue_call 可以给函数传入参数
# job = q.enqueue_call(func=count_words_at_url, args=('http://www.baidu.com',), timeout=2)
# print(job.result)       # None
# time.sleep(2)
# print(job.result)        # 162
# while not job.result:
#     print(job.status)
#     print(job.is_finished)
#     print(job.result)


# print(len(q))
# queue_job_ids = q.job_ids       # 查看队列中的jobid
# queue_jobs = q.jobs             # 查看队列重的job实例
# job = q.fetch_job('c55dad59-ef3c-4080-ad6c-ae07e5475b21')       # 获取job id 为 这个值的job

# print(queue_job_ids, queue_jobs, job)

# q.delete(delete_jobs=True)


# # Job dependencies 依赖其他的job来运行
# # send_report将在generatr_port运行完后才运行
# q = Queue('low', connection=redis_conn)
# report_job = q.enqueue(generate_report)
# q.enqueue(send_report, depends_on=report_job)


