import threading

class SharedCounter:
    def __init__(self,initial_value = 0):
        self._value = initial_value
        self._value_lock = threading.Lock()

    def incr(self,delta=1):
        with self._value_lock:
            self._value += delta

    def decr(self, delta=1):
        with self._value_lock:
            self._value -= delta



# Lock 对象和with语句一块使用可以保证互斥执行，就是每次只有一个线程可以执行with语句包含的代码块。with语句会在这个代码块执行前自动获取锁，在执行结束后自动释放锁
