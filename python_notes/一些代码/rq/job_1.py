from redis import Redis
from rq.job import Job
from rq import Queue
from count_words import count_words_at_url

redis_conn = Redis()
q = Queue('collect', connection=redis_conn)
# job = q.enqueue(count_words_at_url, 'https://github.com', result_ttl=10)

# print(job.id)
print(q)
for id in q.job_ids:
    job = Job.fetch(id, connection=redis_conn)
    print(job.func_name)
    print(job.args)
    print(job.kwargs)
    print(job.result)
    print(job.enqueued_at)
    print(job.started_at)
    print(job.ended_at)
    print(job.exc_info)

# from rq import get_current_job

