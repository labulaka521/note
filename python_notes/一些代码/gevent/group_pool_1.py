import gevent
from gevent.pool import Pool

p = Pool(3)

def hello_from(n):
    print('Size of poll %s' % len(p))

p.map(hello_from, range(5))
