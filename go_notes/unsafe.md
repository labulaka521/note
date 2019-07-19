## unsafe包的作用

unsafe包含三个函数两个自定义类型
- func Sizeof(x ArbitraryType) uintptr
- func Offsetof(x ArbitraryType) uintptr
- func Alignof(x ArbitraryType) uintptr
- type ArbitraryType int
- type Pointer *ArbitraryType


出于安全原因，Golang不允许下面之间的直接转换
- 两个不同指针类型的值，例如int64和float64
- 指针类型和uinptr类型的值

但是使用unsafe.Pointer，可以这样转化
unsafe包文档中列出的规则
- 任何类型的指针都可以转换为unsafe.Pointer
- unsafe.Pointer可以转换为任何类型的指针值
- uintptr可以转换为unsafe.Pointer
- unsafe.Pointer可以转换为uintptr


一个转化的例子
```go
package main

import (
	"fmt"
	"unsafe"
)

func main() {
	var n int64 = 5
	var pn = &n
	var pf = (*float64)(unsafe.Pointer(pn))
	fmt.Println(*pf)
	*pf = 3.15159
	fmt.Println(n)
}

```

unsafe.Pointer和uintptr
- uintptr是一个整数类型
  - 即使uintptr变量仍然有效，由uintptr变量表示的地址处的数据仍然也可能被GC回收
- unsafe.Pointer是一个指针类型
  - unsafe.Pointer值不能被取消引用
  - 如果unsafe.Pointer变量仍有效，则由unsafe.Pointer变量表示的地址处的数据不会被GC回收
  - unsafe.Pointer是一个通用的指针类型，就像* int等。

## 转换T1为T2
对于将T1转换为unsafe.Pointer，然后转换为T2，unsafe的docs中说明了`如果T2比T1大，并且两者共享等效内存布局，则该转换允许将一种类型的数据重新解释为另一类型的数据`

EG:
```go
func main() {
	type MyInt int

	a := []MyInt{0,1,2}
	b := *(*[]int)(unsafe.Pointer(&a))
	b[0] = 3
	fmt.Println(b,a)
	a[2] = 9
	fmt.Println(b,a)
}
```
