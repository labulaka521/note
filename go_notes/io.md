# IO

io.Writer的声明
```go
type Writer interface {
    Write(p []byte) (n int, err error)
}
```
io.Writer接口的文档
>Write 从 p 里向底层的数据流写入 len(p)字节的数据。这个方法返回从 p 里写出的字节 数(0 <= n <= len(p))，以及任何可能导致写入提前结束的错误。Write在返回n < len(p)的时候，必须返回某个非nil值的error。Write绝不能改写切片里的数据， 哪怕是临时修改也不行。

io.Reader的声明
```go
type Reader interface{
    Read(p []byte) (n int, err error)
}
```
>(1) Read最多读入len(p)字节，保存到p。这个方法返回读入的字节数(0 <= n <= len(p))和任何读取时发生的错误。即便Read返回的n < len(p)，方法也可 能使用所有 p 的空间存储临时数据。如果数据可以读取，但是字节长度不足 len(p)， 习惯上 Read 会立刻返回可用的数据，而不等待更多的数据。  
>(2) 当成功读取 n > 0字节后，如果遇到错误或者文件读取完成，Read方法会返回 读入的字节数。方法可能会在本次调用返回一个非 nil 的错误，或者在下一次调用时返 回错误(同时n == 0)。这种情况的的一个例子是，在输入的流结束时，Read会返回 非零的读取字节数，可能会返回err == EOF，也可能会返回err == nil。无论如何， 下一次调用Read应该返回0, EOF。  
>(3) 调用者在返回的n > 0时，总应该先处理读入的数据，再处理错误err。这样才 能正确操作读取一部分字节后发生的 I/O 错误。EOF 也要这样处理。  
>(4) Read的实现不鼓励返回0个读取字节的同时，返回nil值的错误。调用者需要将 这种返回状态视为没有做任何操作，而不是遇到读取结束。