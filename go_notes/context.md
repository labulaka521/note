# Context

```go

type Context interface {
    // 返回截止时间和ok。
	Deadline() (deadline time.Time, ok bool)

    // 返回一个channel。当times out或者调用cancel方法时，将会close掉。
	Done() <-chan struct{}
    // 返回一个错误 为什么该context被取消掉
	Err() error

    // 返回值
	Value(key interface{}) interface{}
}
```

所有的方法
```go
func Background() Context
func TODO() Context

func WithCancel(parent Context) (ctx Context, cancel CancelFunc)
func WithDeadline(parent Context, deadline time.Time) (Context, CancelFunc)
func WithTimeout(parent Context, timeout time.Duration) (Context, CancelFunc)
func WithValue(parent Context, key, val interface{}) Context
```

`context.Background` 返回一个不为nil 空的Context，而且从不会被取消，没有参数 也没有截止日期 主要用于main函数、初始化以及测试代码中，作为Context这个树结构的最顶层的Context，也就是根Context。

`context.TODO` 它目前还不知道具体的使用场景，如果我们不知道该使用什么Context的时候，可以使用这个。  如果你没有 context，却需要调用一个 context 的函数的话，用 context.TODO()

- 不要把Context放在结构体中，要以参数的方式传递
- 以Context作为参数的函数方法，应该把Context作为第一个参数，放在第一位。
- 给一个函数方法传递Context的时候，不要传递nil，如果不知道传递什么，就使用context.TODO
- Context的Value相关方法应该传递必须的数据，不要什么数据都使用这个传递
- Context是线程安全的，可以放心的在多个goroutine中传递

DEMO:  
**WithCancel**  
```go
package main

import (
	"context"
	"fmt"
)
// WithCancel 传递一个父Context作为参数，返回子Context，以及一个取消函数用来取消Context。

func main() {
	gen := func(ctx context.Context) <- chan int {
		dst := make(chan int)
		n := 1
		go func() {
			for {
				select {
				case <- ctx.Done():
					return
				case dst <- n:
					n ++
				}
			}
		}()
		return dst
	}

	ctx, cancel := context.WithCancel(context.Background())

	defer cancel()
	for n := range gen(ctx) {
		fmt.Println(n)
		if n == 5 {
			break
		}
	}
}
```
**WithDeadline**
```go
package main

import (
	"context"
	"fmt"
	"time"
)


// WithDeadline的第二个参数为time.Time类型
func main() {
	d := time.Now().Add(500000 * time.Millisecond)

	ctx, cancel := context.WithDeadline(context.Background(), d)
	defer cancel()

	select {
	case <- time.After(1 * time.Second):
		fmt.Println("oversleept")
	case <-ctx.Done():
		fmt.Println(ctx.Err())
	}
}
```

**WithTimeout**
```go
package main

import (
	"context"
	"fmt"
	"time"
)

// WithTimeout 的第二个参数类型为timeout time.Duration类型
// WithTImeout 调用WithDeadline并将当前时间加上timeout作为第二个参数

func main() {
	// Pass a context with a timeout to tell a blocking function that it
	// should abandon its work after the timeout elapses.
	ctx, cancel := context.WithTimeout(context.Background(), 50*time.Millisecond)
	defer cancel()

	select {
	case <-time.After(1 * time.Second):
		fmt.Println("overslept")
	case <-ctx.Done():
		fmt.Println(ctx.Err()) // prints "context deadline exceeded"
	}
}
```

**WithValue**
```go
package main

import (
	"context"
	"fmt"
)

// WithValue 与取消函数无关它是为了生成一个绑定了一个键值对数据的Context，这个绑定的数据可以通过Context.Value方法访问到


func main() {
	type favContextKey string

	f := func(ctx context.Context, k favContextKey) {
		if v := ctx.Value(k); v != nil {
			fmt.Println(v)
			return
		}
		fmt.Println("Not Found")
	}
	k := favContextKey("language")
	ctx := context.WithValue(context.Background(),k,"GO")
	f(ctx, k)
	f(ctx, favContextKey("GOGOGO"))
}
```