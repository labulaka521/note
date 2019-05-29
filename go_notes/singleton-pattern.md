# Go语言中的单例模式


### 判断是否为nil
```go
package singleton

type singleton struct {
}

var instance *singleton

func GetInstance() *singleton {
	if instance == nil {
		instance = &singleton{}   // 不是线程安全的
	}
	return instance
}
```
不是线程安全的

### 使用Mutex锁

```go
var mu Sync.Mutex

func GetInstance() *singleton {
    mu.Lock()                    // 如果已经创建就没有必要加锁 多余的资源浪费
    defer mu.Unlock()

    if instance == nil {
        instance = &singleton{}
    }
    return instance
}
```
如果实例已经创建我们应该值返回缓存的单例实例。在高并发的代码中，这可能成为瓶颈

### check-lock-check 模式

伪代码
``` go
if check() {
    lock() {
        if ckeck() {
            // 安全执行代码
        }
    }
}
```
先检查，然后获取独占锁, 但是在第一次检查和获取独占锁之间可能有另一个线程确实获得了锁，因此我们需要再次检查锁内部以避免用另一个替换该实例。

使用check-lock-check
```go
func GetInstance() *singleton {
    if instance == nil {     // 不是原子性
        mu.Lock()
        defer mu.Unlock()

        if instance == nil {
            instance = &singleton{}
        }
    }
    return instance
}
```
由于编译器优化，因此没有对实例存储状态进行原子检查。考虑到所有技术因素，这仍然不完美。但它比最初的方法要好得多。

使用`sync/atomic`包,设置一个标志，来标记是否初始化我们的实例
```go
import "sync"
import "sync/atomic"

var initialized uint32
...

func GetInstance() *singleton {

    if atomic.LoadUInt32(&initialized) == 1 {
		return instance
	}

    mu.Lock()
    defer mu.Unlock()

    if initialized == 0 {
         instance = &singleton{}
         atomic.StoreUint32(&initialized, 1)
    }

    return instance
}
```


### 使用sync.Once包

Once包的souce code
```go
// Once is an object that will perform exactly one action.
type Once struct {
	m    Mutex   // 锁
	done uint32  // 标记
}

func (o *Once) Do(f func()) {
	if atomic.LoadUint32(&o.done) == 1 {
		return
	}
	// Slow-path.
	o.m.Lock()
	defer o.m.Unlock()
	if o.done == 0 {
		defer atomic.StoreUint32(&o.done, 1)
		f()
	}
}
```

使用Once的单例模式
```go
package singleton

import (
    "sync"
)

type singleton struct {
}

var instance *singleton
var once sync.Once

func GetInstance() *singleton {
    once.Do(func() {
        instance = &singleton{}
    })
    return instance
}
```
