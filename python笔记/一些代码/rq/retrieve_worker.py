from redis import Redis
from rq import Queue, Worker

redis = Redis()

# 获取worker的信息 rq 
workers = Worker.all(connection=redis)
# print(workers)
for worker in workers:
    print(worker.successful_job_count)
    print(worker.failed_job_count)
    print(worker.total_working_time)

# worker 的总数
worker = Worker.count(connection=redis)
print(worker)

# 计算队列的工作数量
queue = Queue('low', connection=redis)
workers = Worker.count(queue=queue)
print(workers)


# # 获取worker的失败率
# worker = Worker.all_keys(connection=redis)
# print(worker)


# q = Queue('low',connection=redis)
# print(q.count)
# worker = Worker.find_by_key('rq:worker:MacBook-Pro-1.18076', connection=redis)
# print(worker.successful_job_count)
# print(worker.failed_job_count)
# print(worker.total_working_time)
