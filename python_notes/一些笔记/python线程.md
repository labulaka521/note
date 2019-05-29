(GIL)的原因，python的线程被限制到同一时刻只允许一个线程执行这个执行模型。所以,python的线程更适用于处理IO和其他需要并发执行的阻塞操作(比如等待IO，等待从数据库获取数据等等)，而不是需要多处理器并行的计算密集型任务。



线程的一个关键特性都是堵路运行且状态不可预测，如果程序中的其他线程需要通过判断某个线程的状态来确定自已的下一步操作，这是线程同步问题就会变得非常棘手。
为了解决这些问题，我们需要使用threading库中的Event对象。Event对象包含一个可由线程设置的信号标志，它允许线程等待某些时间的发生。在初始情况下，event对象的标志为假。如果有线程等待一个event对象，而这个event都讲的信号标志设置为假，那么这个线程将会被一直阻塞直至该标志为真。一个线程如果将一个event对象的信号标志设置为真，它将唤醒所有等待这个event对象的线程。如果一个线程等待一个已经被设置为真的event对象，那么它将忽略这个时间，继续执行。
```
from threading import Thread, Event import time
# Code to execute in an independent thread
def countdown(n, started_evt): print('countdown starting') started_evt.set()
    while n > 0:
        print('T-minus', n) n -= 1 time.sleep(5)
    # Create the event object that will be used to signal startup
        started_evt = Event()
    # Launch the thread and pass the startup event
        print('Launching countdown')
        t = Thread(target=countdown, args=(10,started_evt)) t.start()
    # Wait for the thread to start
        started_evt.wait() print('countdown is running')
```



## 线程加锁
对多线程程序中的临界区加锁以避免竞争条件

要在多线程程序中使用可变对象，你需要使用threading库中的Lock对象

```
import threading
class SharedCounter: 
    '''
    A counter object that can be shared by multiple threads. 
    '''
    def __init__(self, initial_value = 0):
            self._value = initial_value
            self._value_lock = threading.Lock()
    def incr(self,delta=1): '''
    Increment the counter with locking '''
    with self._value_lock:
                 self._value += delta
    def decr(self,delta=1): '''
    Decrement the counter with locking '''
    with self._value_lock:
                 self._value -= delta
```


## 防止死锁的加锁机制
线程需要一次获取多个锁，此时如何避免死锁问题

再多线程程序中，死锁问题很大一部分是由于线程同时获取多个锁造成的。

解决死锁的问题的一种方案是为程序中的每一个锁分配一个唯一的id，然后只允许按照升序规则来使用多个锁。



## python的全局锁GIL

GIL最大的问题就是python多线程程序并不能利用多核CPU的优势(比如一个使用了多个线程的计算密集型程序只会在一个单CPU上面执行)  
GIL只会影响到严重依赖CPU的程序，对于涉及到IO，比如网络交互，那么使用多线程比较合适，因为大部分时间都在等待网络IO


## 什么叫线程安全

当多个线程同时运行时，保证运行结果符合预期，就是线程安全的。由于多线程的执行时，存在线程的切换，而python线程的切换时机是不确定的。既有cooperative multitasking的调度，也有preemptive multitasking的调度
>python线程什么时候切换呢？当一个线程开始sleep或者进行IO操作时，另一个线程就有机会拿到GIL锁，开始执行代码

"原子操作(atomic operation)是不需要synchronized"，这是多线程编程的老生常谈了。 所谓原子操作是指不会被线程调度机制打断的操作；这种操作一旦开始，就一直运行到结束，中间不会有任何context switch （切 换到另一个线程）。

日志记录模块旨在是线程安全的，无需客户完成任何特殊工作。它通过使用线程锁实现了这一点; 有一个锁可以序列化对模块共享数据的访问，每个处理程序还会创建一个锁，以序列化对其底层I / O的访问。

如果使用该signal 模块实现异步信号处理程序，则可能无法在此类处理程序中使用日志记录。这是因为threading模块中的锁实现并不总是可重入的，因此不能从这样的信号处理程序中调用
