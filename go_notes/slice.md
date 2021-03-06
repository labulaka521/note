## 内部实现
切片是围绕动态数组的概念构建的，可以按需自动增长和缩小。底层数据也是连续块中分配的。

切片是一个很小的对象，对底层数组进行了抽象，并提供相关的操作方法。

切片有三个字短的数据结构
- 指向底层数组指针
- 切片的长度
- 切片的容量

```
struct Slice
{                        // must not move anything
    byte*    array;
    uintgo   len;
    uintgo   cap;
};
```

切片的内部实现
![click](../image/slice1.png)

## 创建和初始化

```
slice := make([]string, 3, 5)
```
定义整形切片 长度为3，容量为5个元素

如果基于这个切片创建新的切片，新 切片会和原有切片共享底层数组，也能通过后期操作来访问多余容量的元素。

可以访问3个元素，而底层数组拥有五个元素。剩下的2个元素可以在后期操作中合并到切片，可以通过切片访问到这些元素。
如果基于这个切片创建新的切片，**新切片和原有切片共享底层数组**

### nil切片  
`var slice []int` 

内部实现: ![click](../image/slice2.png)   

**常用于函数要求返回一个切片但是发生异常的时候**  

共享同一底层数组的两个切片
![](../image/slice.jpg)

`newSlice无法访问到它所指向的底层数组的第一个元素的部分`

### 声明空切片  
`slice := make([]int, 0)`  
`slice := []int{}`  

 内部实现: ![click](../image/slice3.png)

创建一个新的切片就是把底层数组切出一部分

### 使用三个索引创建切片  
`slice := source[2:3:4]`  
长度为3-2  
容量为4-2

使用`...`运算符，可以将一个切片的所有元素追加到另一个切片中

range创建了每个元素的副本  

### 多维切片  
`slice:= [][]int{{10}, {100, 200}}`  
内部实现:
![click](../image/slice4.png)

在函数见传递切片就是要在函数间以值的方式传递切片。由于切片的尺寸很小，在函数间复制和传递切片成本也很低。

在`64`位架构的机器上，一个切片需要`24字节`的内存:
- 指针字段需要8字节
- 长度和容量分别需要8字节

与切片关联的数据包含在`底层数组`里，不属于`切片`本身，所以将切片复制到任意函数，对底层数组大小都不会有影响。




## 切片的内部
[原文](https://blog.golang.org/go-slices-usage-and-internals)

切片内部是数组短的描述符
由指向数组的指针，段的长度及其容量组成。

ptr为指向数组的指针
len为数组的长度
cap为数组的容量

---
ptr|len|cap
-|-|-

长度是切片引用的元素数。容量是底层数组中元素的数量。

切片不会复制切片的数据。它创建一个指向原始数组的新切片值。修改重新切片的元素（而不是切片本身）会修改原始切片的元素


# growslice函数 
`/usr/local/go/src/runtime/slice.go:line:98`  

```go
func growslice(et *_type, old slice, cap int) slice {
    newcap := old.cap           // 旧的容量
	doublecap := newcap + newcap        // 旧容量两杯
	if cap > doublecap {        // 如果期望的容量大于当前容量的两倍 则直接使用期望容量
		newcap = cap
	} else {                
		if old.len < 1024 {     // 如果当前容量小于1024 则直接将容量翻倍
			newcap = doublecap
		} else {
			// Check 0 < newcap to detect overflow
			// and prevent an infinite loop.
			for 0 < newcap && newcap < cap {        // 如果当前容量大于1024则每次增加当前容量的1/4 直到新容量大于期望容量
				newcap += newcap / 4
			}
			// Set newcap to the requested cap when
			// the newcap calculation overflowed.
			if newcap <= 0 {
				newcap = cap
			}
		}
    }
}
```

