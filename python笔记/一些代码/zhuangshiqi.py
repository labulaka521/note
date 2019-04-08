from functools import wraps
import time
def run_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func()
        runtime = time.time()-start
        print(tuntime)
        return result
    return wrapper


def timethis(func):
    '''
    Decorator that reports the execution time.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, end-start)
        return result
    return wrapper

@timethis
def countdown(n):
    while n > 0:
        n -= 1

timethis(countdown)

countdown(1000)

print(countdown.__name__)
print(countdown.__doc__)
print(countdown.__annotations__)


# 如果没有@wraps就会备足昂时期函数丢失了所有有用的信息

```
wrapper
None
{}
```

def allow_accoss_domain(func):
    @wraps(func)
    def wapper(*args,**kwargs):
        result = func(*args, **kwargs)
        return result
    return wapper

