def consumer():
    r = ''
    while True:
        print('-'*20)
        n = yield r
        if not n:
            return
        print('[CONSUMER] consuming %s ...' % n)
        r = '200 OK'


def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n += 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCE] Consumer return: %s' % r)
    c.close()


c = consumer()
produce(c)

