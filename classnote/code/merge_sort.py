def mergesort(lst):
    '递归分解序列'
    if len(lst) < 2:
        return lst
    mi = len(lst)//2
    left = mergesort(lst[:mi])
    right = mergesort(lst[mi:])
    merge(left, right)
def merge(left, right):
    '合并序列部分'
    i,j = 0 , 0
    result = []
    while len(left) > 0 and len(right) > 0:
        if left[i]<right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(left[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result
