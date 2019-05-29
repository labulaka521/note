go 实现生产者消费者模式

```
package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
)

// 生产者
func Producer(factor int, out chan<-int) {
	for i := 0; ; i++ {
		out <- i * factor
	}
}

// 消费者
func Consumer(in <-chan int) {
	for v := range in {
		fmt.Println(v)
	}
}

func main() {
	ch := make(chan int, 64)

	go Producer(3, ch)
	go Producer(5, ch)
	go Consumer(ch)

	// 5秒后退出
	//time.Sleep(5 * time.Second)

	sig := make(chan os.Signal, 1)
	signal.Notify(sig, syscall.SIGINT, syscall.SIGTERM)
	fmt.Printf("quit (%v)\n", <-sig)
}
```
