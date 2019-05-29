def fib(n):
    if n<2:
        return n
    g,f=1,0
    for i in range(n-2):
        g = g+f
        f = g-f
    return g 
