## pprof 工具的使用

### pprof画像
pprof的工作方式是使用画像(profiles)

画像是一组显示导致特定事件实例的调用堆栈的追踪

源码[pprof.go](https://golang.org/src/runtime/pprof/pprof.go)  

go有几个内置画像供我们在常见情况下使用

- allocs：过去所有内存分配的样本
- block：导致阻塞同步原语的堆栈跟踪
- cmdline：当前程序的命令行调用
- goroutine：堆叠所有当前goroutine的痕迹
- heap：活动对象的内存分配示例。 您可以指定gc GET参数以在获取堆样本之前运行GC。
- mutex：堆叠争用互斥体持有者的痕迹
- profile：CPU配置文件。 您可以在秒GET参数中指定持续时间。 获取配置文件后，使用go tool pprof命令调查配置文件。
- threadcreate：导致创建新OS线程的堆栈跟踪
- trace：当前程序的执行跟踪。 您可以在秒GET参数中指定持续时间。 获取跟踪文件后，使用go tool trace命令调查跟踪。

### 堆
操作系统存储代码中对象占用内存的地方，这块内存随后会被“垃圾回收”，或者在飞垃圾回收语言中手动释放

堆不是唯一发生内存分配的地方，一些内存在栈中分配。  
栈主要是`短周期`的内存  
在`Go`语言中，`栈`通常用户在`函数闭包`内发生的赋值  

对数据需要手动释放和垃圾回收，而栈数据不需要。栈效率高
  
### 使用pprof

pprof的两种主要的内存分析策略  
- innuse 查看当前的内存分配(字节或者对象计数)
- alloc 查看整个程序运行时的所有内存分配的字节或对象计数

获取堆数据
```
go tool pprof http://localhost:8070/debug/pprof/heap
```
```
inuse_space.003.pb.gz
Type: inuse_space
Time: May 26, 2019 at 3:42pm (CST)
Entering interactive mode (type "help" for commands, "o" for options)
(pprof)
```

Type 的值有
- innuse_space  
已分配但尚未释放的内存数量
- innuse_objects
已分配但尚未释放的对象数量
- alloc_space
已分配的内存总量（不管是否已释放）
- alloc_objects
已分配的对象总量（不管是否已释放）

查询顶级内存的消费者

```
(pprof) top
Showing nodes accounting for 2075.72kB, 100% of 2075.72kB total
Showing top 10 nodes out of 28
      flat  flat%   sum%        cum   cum%
  528.17kB 25.44% 25.44%   528.17kB 25.44%  bufio.NewReaderSize
  521.37kB 25.12% 50.56%   521.37kB 25.12%  encoding/xml.init
  513.56kB 24.74% 75.30%   513.56kB 24.74%  regexp/syntax.init
  512.62kB 24.70%   100%   512.62kB 24.70%  regexp/syntax.(*compiler).inst (inline)
         0     0%   100%   521.37kB 25.12%  github.com/gin-gonic/gin.init
         0     0%   100%   521.37kB 25.12%  github.com/gin-gonic/gin/binding.init
         0     0%   100%   513.56kB 24.74%  github.com/gomodule/redigo/redis.init
         0     0%   100%  1033.99kB 49.81%  golang_cron/common.init
         0     0%   100%   513.56kB 24.74%  golang_cron/common/db/goredis.init
         0     0%   100%   513.56kB 24.74%  golang_cron/master/mgr/emailmgr.init

```

- flat 表示堆栈中当前层函数的内存
- cum 表示堆栈中直到档期函数所累计的内存

实例


```go
// 启动pprof的
_ "net/http/pprof"

func() {
    go func() {
        http.ListenAndServe(":8080", nil)
    }
}
```
```shell
# 查看程序占用的内存
go tool pprof --http=:8081 http://127.0.0.1:8080/debug/pprof/heap
# 自动打开浏览器 有多种查看程序占用内存的方式 就可以定位到程序的哪一块使用的内存比较多

查看程序占用的CPU
go tool pprof --http=:8081 http://127.0.0.1:8080/debug/pprof/profile
## 与上面一样
```


