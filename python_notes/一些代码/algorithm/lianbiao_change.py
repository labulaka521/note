from lianbiao import LList, Lnode, LinkedListUnderflow
from random import randint


class LList1(LList):        # 单链表的简单变形 加入引用最后一个元素
    def __init__(self):
        LList.__init__(self)
        self._rear = None

    def prepend(self, elem):
        if self._head is None:
            self._head = Lnode(elem, self._head)
            self._rear = self._head
        else:
            self._head = Lnode(elem, self._head)

    def append(self, elem):
        if self._head is None:
            self._head = Lnode(elem, self._head)
            self._rear = self._head
        else:
            self._rear.next = Lnode(elem)
            self._rear = self._rear.next


    def pop_last(self):
        if self._head is None:
            return LinkedListUnderflow("in pop_last")
        p = self._head
        if p.next is None:      #只有一个元素
            e = p.elem
            self._head = None
            return e
        while p.next.next is not None:
            p = p.next
        e = p.next.elem
        p.next = None
        return e

    def rever(self):
        '单链表反转'
        p = None                                # 初始化新链表为None
        while self._head is not None:
            l = self._head                      # 记录当前的头节点 此节点
            self._head = l.next                 # 后移当前的头节点
            l.next = p                          # 设置新链表的尾部链表为p
            p = l                               # 更新当前的链表
        self._head = p


    def sort1(self):
        # 与前面的一直比较，放入合适的位置，然后crt往后移动。 与插入排序类似
        if self._head is None:
            return
        crt = self._head.next                   # 从节点的首的下一个节点开始
        while crt is not None:                  # 节点存在继续
            x = crt.elem                        # 记录当前节点的值
            p = self._head                      # 比较的首节点
            while x > p.elem and p is not crt:  # 当x大于比较的节点并且当前的比较节点不等于crt 就将比较元素后移一位
                p = p.next
            while p is not crt:                 # 已经寻找到需要替换的数据      # 这个while循环使一个值就位
                y = p.elem                      # 记录当前被替换节点的值
                p.elem = x                      # 给当前节点赋值
                x = y                           # 记录下当前被替换节点的值
                p = p.next                      # 转下被替换节点的下一节点继续替换
            crt.elem = x
            crt = crt.next

    def sort2(self):        # 通过调节链接的方式
        # self._head始终是已经排序的，用rem表示除首元素的元素，然后后面的元素依次与此结点比较，插入合适的位置，
        p  = self._head
        if p is None or p.next is None:
            return p
        rem = p.next
        p.next = None
        while rem is not None:
            p = self._head
            # print(p)
            q = None
            while p is not None and p.elem < rem.elem:
                q = p
                p = p.next
            if q is None:
                self._head = rem
            else:
                q.next = rem
            q = rem
            rem = rem.next
            q.next = p
            self.printall()




mlist1 = LList1()
# mlist1.prepend()
for i in range(3):
    mlist1.append(randint(1,20))
mlist1.printall()
mlist1.sort2()
mlist1.printall()
# for x in mlist1.filter(lambda y: y % 2 == 0):
#     print(x)



# def lst_sort(lst):
#     for i in range()
# a = [1,2,3,4,5]





