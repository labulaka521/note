from lianbiao import Lnode, LinkedListUnderflow

# 循环单链表

class LCList:
    def __init__(self):
        self._rear = None

    def is_empty(self):
        return self._rear is None

    def prepend(self, elem):        #前端加入
        p = Lnode(elem)
        if self._rear is None:  #  链表为空
            p.next = p
            self._rear = p
        else:
            p.next = self._rear.next
            self._rear.next = p

    def append(self, elem): # 尾端插入
        self.prepend(elem)      # 使用前段插入，然后将self._rear设置为前端第一个元素  也就是self._rear = self._rear.next
        self._rear = self._rear.next

    def pop(self):
        if self._rear is None:
            return LinkedListUnderflow("in pop")
        p = self._rear.next
        if self._rear is p:
            self._rear = None
        else:
            self._rear.next = p.next
        return p.elem

    def pop_last(self):
        if self._rear is None:
            return LinkedListUnderflow('in pop_last')
        p = self._rear.next
        if self._rear is p:
            self._rear = None
            return p.elem
        else:
            p1 = self._rear.next        # 记录单链表的头
            while p.next is not self._rear:     #  从前往后循环 当循环到最后一个元素时退出
                p = p.next
            e = p.next.elem                 # 记录最后一个元素的值
            self._rear = p                  # 设置弹出后的链表的最后一个元素
            self._rear.next = p1            # 设置表尾与表头的连接
            return e



    def printall(self):
        if self.is_empty():
            return
        p = self._rear.next
        while True:
            print(p.elem, end='， ')
            if p is self._rear:
                return
            p = p.next
# lclist = LCList()
# for i in range(5):
#     lclist.prepend(i)
# # print(lclist.pop_last())
# lclist.printall()
