# 数组求和 二分递归 分而治之

def sub(lst,lo,hi):
    if lo == hi:
        return lst[lo]
    mi = (lo + hi)//2
    return sub(lst,lo,mi)+sub(lst,mi+1,hi)

print(sub([1, 2, 3, 4, 5],0,4))
