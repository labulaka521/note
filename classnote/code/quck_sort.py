def quick_sort(lst,start, end):
    '''快速排序的思想就是先找到一个数作为参考点，然后遍历，将比这个参考点小的数移到左边
       将比这个参考点大的数移到右边，
       先从左边第一个点开始向右查找，当遇到比参考点大的数就停止，
       然后从最右端向左遍历，当遇到参考点小的也停止，
       然后交换这两个点，然后继续重复上述过程直到两点相遇退出循环
       然后将参考点与相遇点的值互换。此时参考点的前半部分就是比参考点小的元素，后半部分就是比参考点大的元素
       然后将参考点前的元素，和参考点后的元素分别递归循环。
    '''
    if start>end:
        return 0
    flag = lst[start]                               # 选择参考点
    left = start                                    # 作出
    right = end
    while start<end:
        while flag < lst[end] and start < end:
            end -= 1
        while lst[start] <= flag and start < end:
            start += 1
        lst[end], lst[start] = lst[start], lst[end]
    lst[left], lst[start] = lst[start], lst[left]
    quick_sort(lst, left, start - 1)
    quick_sort(lst, start + 1, right)


def main():
    lst = [6, 3, 10, 5, 1, 9, 2, 7, 23, 4, 14]
    quick_sort(lst, 0, len(lst) - 1)
    print(lst)
main()

