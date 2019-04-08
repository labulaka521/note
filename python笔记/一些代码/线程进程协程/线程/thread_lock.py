import threading

class Counter:
    def __init__(self, initial_value = 0):
        self._value = initial_value
        self._value_lock = threading.lock()
    

    def incr(self, delta=1):
        with self._value_lock:
            self._value += delta

    
    def decr(self, delta=1):
        with self._value_lock:
            self_value  -= delta



# RLock 被称为可重入锁 它可以被同一个线程多次获取，主要编写基于锁的代码
# 只有一个作用于整个类的锁，它被所有的类实例锁共享。不再将所绑定到每个实例的可变状态上，
# 这个实现的特点之一就是无论创建了多少了counter实力，都只会有一个锁的存在，因此对内存的使用效率会很高
class Counter:
    _lock  = threading.RLock()
    def __init__(self, initial_value = 0):
        self._value = initial_value

    def incr(self, delta=1):
        with Counter._lock:
            self._value += 1

    def decr(self, delta=1):
        with Counter._lock:
            self._value -= 1


class X:
    def __init__(self):
        self.a = 1
        self.b = 2
        self.lock = threading.RLock()

    def changeA(self):
        with self.lock:
            self.a = self.a + 1

    def changeB(self):
        with self.lock:
            self.b = self.b + self.a

    def changeAandB(self):
        # you can use chanceA and changeB threadsave!
        with self.lock:
            self.changeA()  # a usual lock would block in here
            self.changeB()

x = X()
x.changeAandB()
