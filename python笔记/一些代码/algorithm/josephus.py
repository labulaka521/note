#  假设有n个人围坐一圈，现在要求从k个人开始报数，报到第m个数的人退出。然后从下一个开始继续报数并按同样规则退出，直至所有人退出。要求顺序输出各列人的编号


def josephus(n, k, m):

        people = list(range(1, n+1))
        i = k - 1
        for num in range(n):
            count = 0
            while count < m:
                if people[i]>0:
                    count += 1
                if count == m:
                    print(people[i], end="")
                    people[i] = 0
                i = (i+1) % n
            if num < n -1:
                print(", ",end="")
            else:
                print("")


def josephus_a(n, k,m):
    people = n
    while len(n) > 1:               # 当列表中只剩一个元素时退出循环
        k = (k - 1 + m ) % len(n)   # 往后移动m步
        # 因为第一个元素是的位置是1，所以每次计算出列人的时候需要减1才是列表中元素的位置，
        # 每次弹出一个元素后，则开始计数的位置为被删除元素的位置，而这时需要将当前位置-1 然后加上步数才是下次需要弹出元素的位置
        print(p)
    print(people[0])

l = ['余', '廖', '李', '宋', '黄', '梁', '冠']


k = int(input())
m = int(input())
# josephus_a(l,k,m)
print(len(l))
josephus_a(l,k,m)
# test(l, k)
