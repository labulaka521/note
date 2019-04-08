# 进程
当运行一个 应用程序(如一个 IDE 或者编辑器)的时候，操作系统会为这个应用程序启动一个进程。可以将 这个进程看作一个包含了应用程序在运行中需要用到和维护的各种资源的容器

一个线程是一个执行空间，这个空间会被操作系统调度来运行 函数中所写的代码。每个进程至少包含一个线程，每个进程的初始线程被称作主线程。因为执行 这个线程的空间是应用程序的本身的空间，所以当主线程终止时，应用程序也会终止。

# 并发
当一个函数创建为goroutine时，Go会将其是做一个独立的工作但愿。这个单元会被调度道可用的逻辑处理器上执行。
用于在 goroutine 之间同步和传递数据的关键数据类型叫作通道 (channel)。

在 1.5 版本 1上，Go语言的 运行时默认会为每个可用的物理处理器分配一个逻辑处理器。在 1.5 版本之前的版本中，默认给 整个应用程序只分配一个逻辑处理器。

go语言运行时会把goroutine调度到逻辑处理器上运行。这个逻辑处理器绑定到唯一的操作系统线程。当goroutinr可以运行的时候会被放入逻辑处理器的执行队列中。
[click](https://www.dropbox.com/s/7w5n4wh983pm2iq/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202019-02-27%2011.51.20.png?dl=0)

当goroutine执行了一个阻塞的系统调用时，调度器会将这个线程与处理器分离，并创建一个新线程来运行这个处理器上提供的服务
[click](https://www.dropbox.com/s/hmibyol72lr2k6i/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202019-02-27%2011.53.08.png?dl=0)

调度器对可以创建的逻辑处理器没有限制，但语言运行时默认限制每个程序最多创建10000个线程。这个限制值可以通过调用`runtime/debug`的`SetMaxThreads`方法来更改。

如果让希望让goroutine并行，必须使用多于一个逻辑处理器。当有多个逻辑处理器时，调度器会将goroutine平等分配到每个逻辑处理器上。

### goroutine
基于调度器的内部算法，一个正在运行的goroutine在工作结束前，可以被停止并重新调度。调度器这样做的目的是防止某个goroutine长时间占用逻辑处理器。当goroutine占用时间过长时，调度器会停止当前运行的goroutine，并给其他可运行的goroutine运行的机会
[click](https://www.dropbox.com/s/x15b7a89jwxev1g/%E5%B1%8F%E5%B9%95%E6%88%AA%E5%9B%BE%202019-02-27%2016.43.50.png?dl=0)

### 竞争状态

对一个共享资源的读写操作必须是原子化的
同一时间只能有一个goroutine对共享资源进行读和写操作

> Gosched生成处理器，允许其他goroutine运行。它不
>暂停当前的goroutine，这样执行将自动恢复。
runtime.Gosched()

go build --race 启用数据竞态检测。

### 锁住共享资源


原子操作
加1
atomic.AddInt64(&counter, 1)

将1赋值给shutdown
atomic.StoreInt64(&shutdown, 1)

读取值
atomic.LoadInt64(&shutdown)


- 并发是指 goroutine 运行的时候是相互独立的。
- 使用关键字 go 创建 goroutine 来运行函数。
- goroutine 在逻辑处理器上执行，而逻辑处理器具有独立的系统线程和运行队列。 
- 竞争状态是指两个或者多个 goroutine 试图访问同一个资源。 
- 原子函数和互斥锁提供了一种防止出现竞争状态的办法。 
- 通道提供了一种在两个 goroutine 之间共享数据的简单方法。 
- 无缓冲的通道保证同时交换数据，而有缓冲的通道不做这种保证。

goroutine 调度器

>调度就是决定何时哪个goroutine将获得资源开始执行、哪个goroutine应该停止执行让出资源、哪个goroutine应该被唤醒恢复执行等。

将goroutines按照一定算法放到不同的操作系统线程中去执行。

[知乎: Golang 的 goroutine 是如何实现的？](https://www.zhihu.com/question/20862617/answer/27964865)    
[也谈goroutine调度器](https://tonybai.com/2017/06/23/an-intro-about-goroutine-scheduler/)


Go的调度器内部有三个重要的结构
- M  
代表真正的内核OS线程，和POSIX里的thread差不多，真正干活的。M代表着真正的执行计算资源。在绑定有效的p后，进入schedule循环；而schedule循环的机制大致是从各种队列、p的本地队列中获取G，切换到G的执行栈上并执行G的函数，调用goexit做清理工作并回到m，如此反复。M并不保留G状态，这是G可以跨M调度的基础。
- G  
代表一个goroutine，它有自已的栈，instruction pointer和其他信息(正在等待的channel等等)，用于调度。G对象是可以重用的。
- P  
代表调度的上下文，它可以把它看做一个局部的调度器，使go代码在一个线程上跑，它是实现N：1 到N：M映射的关键 。表示逻辑processor，P的数量决定了系统内最大可并行的G的数量（前提：系统的物理cpu核数>=P的数量）；P的最大作用还是其拥有的各种G对象队列、链表、一些cache和状态。

![](https://pic1.zhimg.com/80/67f09d490f69eec14c1824d939938e14_hd.jpg)


