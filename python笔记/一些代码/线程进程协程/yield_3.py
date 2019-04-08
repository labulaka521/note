def h(): 
    print('Wen Chuan,')
    m = yield 5  # Fighting!
    print(m)
    d = yield 12
    print('We are together!')

c = h()
m = next(c)
d = c.send('Fighting!')  
# c.send的返回值是下一个yield表达式的参数
print('We will never forget the date', m, '.', d)
