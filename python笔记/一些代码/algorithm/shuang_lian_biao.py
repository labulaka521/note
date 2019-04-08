# 双链表
from lianbiao import Lnode, LinkedListUnderflow
from lianbiao_change import LList1

class DLNode(Lnode):        # 双链表结点类
    def __init__(self, elem, prev=None, next_=None):
        Lnode.__init__(self, elem, next_)
        self.prev = prev

class DLList(LList1):        # 单项双链表
    def __init__(self):
        LList1.__init__(self)

    def prepend(self, elem):
        p = DLNode(elem, None, self._head)          # 在前端加入元素的话此元素的next应该是原来链表的顶部，所以在此定义元素时应该将self.next_设置为self._head
        if self._head is None:
            self._rear = p
        else:
            p.next.prev = p
        self._head = p

    def append(self, elem):
        p = DLNode(elem, self._rear, None)          # 与上面相反 此元素前一个元素是self._rear  self.prev = self._rear
        if self._head is None:
            self._head = p
        else:
            p.prev.next = p
        self._rear = p

    def pop(self):
        if self._head is None:
            return LinkedListUnderflow("in pop")
        e = self._rear.elem
        self._head = self._head.next
        if self._head is not None:
            self._head.prev = None
        return e

    def pop_last(self):
        if self._head is None:
            return LinkedListUnderflow("in pop_last")
        e = self._rear.elem
        self._rear = self._rear.prev
        if self._rear is not None:
            self._rear.next = None
        return e
while index == 0 or index == len(items):


class DDList(DLList):       # 循环双链表

    def __init__(self):
        DLList.__init__(self)

    def prepend(self, elem):
        p = DLNode(elem, self._rear, self._head)
        if self._head is None:
            self._rear = p
        else:
            p.next.prev = p
            p.prev.next = p
        self._head = p

    def append(self, elem):
        p = DLNode(elem, self._rear, self._head)
        if self._head is None:
            self._head = p
        else:
            p.prev.next = p
            p.next.prev = p
        self._rear = p

    def pop(self):
        if self._head is None:
            return LinkedListUnderflow('in pop')
        if self._head.next is self._head:
            self._head = None
            self._rear = None
        else:
            e = self._head.elem
            self._head = self._head.next
            self._head.prev = self._rear
            self._rear.next = self._head
        print(e)
        return e

    def pop_last(self):
        if self._head is None:
            return LinkedListUnderflow('in pop_last')
        if self._rear.next is self._rear:
            self._rear = None
            self._head = None
        else:
            e = self._rear.elem
            self._rear = self._rear.prev
            self._rear.next = self._head
            self._head.prev = self._rear
        print(e)
        return e
    def printall(self):
        if self.is_empty():
            return
        p = self._head
        print(p.elem, end=', ')
        while p.next is not self._head:
            print(p.next.elem, end=', ')
            p = p.next

ddlist = DDList()
for i in range(10):
    ddlist.append(i)
ddlist.pop_last()
ddlist.pop()
ddlist.pop_last()
ddlist.pop()
ddlist.printall()












