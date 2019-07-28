## 什么是channel
cannel和goroutinue是go语言并发编程的两大基石，Goroutinue用于执行并发任务，channel用于foroutinue之间的同步

channel在goroutinue间架起了一条管道，在管道里传输数据，实现goroutinue间的通信，由于它是线程安全的，channel 还提供“先进先出”的特性；它还能影响 goroutine 的阻塞和唤醒。

## 为什么要channel
Go通过channel实现CSP通信模型，主要用于goroutinue之间的消息传递和事件通知

有了 channel 和 goroutine 之后，Go 的并发编程变得异常容易和安全，得以让程序员把注意力留到业务上去，实现开发效率的提升

## channel实现原理
channel分为两种
- 带缓冲  
  同步模型，必须发送方和接收方配对操作才会成功，否则会被阻塞  
- 不带缓冲  
  异步模型，缓冲草要有剩余容量，操作才会成功，否则也会被阻塞  

```go
type hchan struct {
	qcount   uint           // 缓冲槽有效数据数量
	dataqsiz uint           // 缓冲槽大小
	buf      unsafe.Pointer // 缓冲槽指针 只有缓冲型channel才有 指向底层循环数组的指针
	elemsize uint16         // 数据项大小
	closed   uint32         // 是否关闭
	elemtype *_type         // 数据项类型
	sendx    uint           // 已发送元素在循环数组中的索引值
	recvx    uint           // 已接收元素在循环数组中的索引值
	recvq    waitq          // 接收者等待队列
	sendq    waitq          // 发送者等待队列

	lock mutex
}
```
![](../image/channel.png)

```go
func makechan(t *chantype, size int) *hchan {

    var c *hchan
	switch {
	case size == 0 || elem.size == 0:
        // Queue or element size is zero.
        // size为0
		c = (*hchan)(mallocgc(hchanSize, nil, true))
		// Race detector uses this location for synchronization.
		c.buf = c.raceaddr()
	case elem.kind&kindNoPointers != 0:
		// Elements do not contain pointers.
		// Allocate hchan and buf in one call.
		c = (*hchan)(mallocgc(hchanSize+uintptr(size)*elem.size, nil, true))
		c.buf = add(unsafe.Pointer(c), hchanSize)
	default:
		// Elements contain pointers.
		c = new(hchan)
		c.buf = mallocgc(uintptr(size)*elem.size, elem, true)
    }
}
```

## 应用
- 停止信号
- 任务定时
- 解藕生产方和消费房
- 控制并发数

