from random import randrange
def sort(lst):
    for j in range(1, len(lst)):
        x = lst[j]
        i = j
        while i > 0 and lst[i-1] > x:
            lst[i] = lst[i-1]
            i -= 1
        lst[i] = x
a = []
for i in range(1000):
    a.append(randrange(1,1000))
print(a)
sort(a)
print(a)
