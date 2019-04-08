def h():
    print('Wen Chuan')
    yield 5
    print('Fighting!')

c = h()
next(c)
c.__next__()
