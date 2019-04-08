#### 变长的函数参数
如果**最后一个**函数参数的类型的是...T，那么在调用这个函数的时候，我们可以在参数列表的最后使用若干个类型为T的参数。这里，...T在函数内部的类型实际是[]T.

```go
func Sum(nums ...int) int {
    res := 0
    for _, n := range nums {
        res += n
    }
    return res
}

Sum(1,2,3)
```

#### 调用拥有变长参数列表的函数
上面调用Sum函数时，是将变长参数分开写的。如果我们有一个slice，那么我们调用时不必将slice拆开再调用，直接在slice后跟...即可：

```go
primes := []int{2, 3, 5, 7}
fmt.Println(Sum(primes...)) // 17
```

#### 标识数组元素个数
这里，...意味着数组的元素个数：

```go
stooges := [...]string{"Moe", "Larry", "Curly"} // len(stooges) == 3
```

#### Go命令行中的通配符
描述包文件的通配符。
在这个例子中，会单元测试当前目录和所有子目录的所有包：

```
go test ./...
```