

def selectsort(lst):
    '选择排序'
    length = len(lst)
    for i in range(length):
        min = i
        for j in range(i, length):
            if lst[min] > lst[j]:
                min = j
        lst[i],lst[min] = lst[min], lst[i]
        print(lst)
lst = [int(i) for i in input().split()]
selectsort(lst)
