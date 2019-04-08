# 数组求和 线性递归
def sub(lst,n):
    if n == 1:
        return lst[0]
    return sub(lst,n-1)+lst[n-1]


print(sub([1,2,3,4,5],5))
