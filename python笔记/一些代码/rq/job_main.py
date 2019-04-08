from rq.decorators import job
from redis import Redis

redis_conn = Redis()


@job('low', connection=redis_conn, timeout=5)
def add(x, y):
    return x + y
