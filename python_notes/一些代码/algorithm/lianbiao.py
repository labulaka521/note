class Lnode:
    def __init__(self, elem, next_=None):
        self.elem = elem
        self.next = next_

class LinkedListUnderflow(ValueError):
    pass


class LList:        # 单链表类
    def __init__(self):
        self._head = None

    def is_empty(self):
        '链表为空'
        return self._head is None


    def prepead(self, elem):
        '首部加入'
        self._head = Lnode(elem, self._head)

    def filter(self, pred):
        '查找'
        p = self._head
        while p is not None:
            if pred(p.elem):
                yield p.elem
            p = p.next

    def pop(self):
        '弹出最后首元素'
        if self._head is None:
            return LinkedListUnderflow("in pop")
        e = self._head.elem
        self._head = self._head.next
        return e

    def append(self, elem):
        '尾部添加元素'
        if self._head == None:
            self._head = Lnode(elem)
            return
        p = self._head
        while p.next is not None:                       # 寻找尾部
            p = p.next
        p.next = Lnode(elem)

    def pop_last(self):
        '尾部弹出元素'
        if self._head is None:
            return LinkedListUnderflow("in pop_last")
        p = self._head
        if p.next is None:
            e = p.elem
            self._head = None
            return e
        while p.next.next is not None:                  # 寻找尾部    
            p = p.next
        e = p.next.elem
        p.next = None
        return e

    def printall(self):
        p = self._head
        while p is not None:
            print(p.elem, end=' ')
            if p.next is not None:
                print(', ', end='')
            p = p.next
        print(' ')

# mlist1 = LList()
# #
# for i in range(10):
#     mlist1.prepead(i)
# for i in range(11, 20):
#     mlist1.append(i)
# # print(mlist1.next_.elem)
# mlist1.printall()
