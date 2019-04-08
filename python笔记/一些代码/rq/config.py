## worker 的配置文件

REDIS_URL = 'redis://127.0.0.1:6379/1'

# You can also specify the Redis DB to use
# REDIS_HOST = 'redis.example.com'
# REDIS_PORT = 6380
# REDIS_DB = 3
# REDIS_PASSWORD = 'very secret'

# 监听的队列
QUEUES = ['high', 'normal', 'low']


# 自定义worker名称
NAME = 'worker-custom'

# rq worker -c config
