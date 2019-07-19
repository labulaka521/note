Interface接口实现

iface 和 eface 都是 Go 中描述接口的底层结构体，区别在于 iface 描述的接口包含方法，而 eface 则是不包含任何方法的空接口：interface{}

## eface
eface的结构
```go
// runtime/runtime2
type eface struct {
	_type *_type
	data  unsafe.Pointer
}
```
`eface`的`_type`字段表示所指对象的类型
`data`表示指向数据的指针
_type字段实现
```go
type _type struct {
    // 类型大小
    size       uintptr
    // 存储所有指针的内存前缀的大小
    ptrdata    uintptr
    // 类型的hash
    hash       uint32
    // 
    tflag      tflag
    // 类型的对其方式
	align      uint8
	fieldalign uint8
	kind       uint8
	alg        *typeAlg
	// gcdata stores the GC type data for the garbage collector.
	// If the KindGCProg bit is set in kind, gcdata is a GC program.
    // Otherwise it is a ptrmask bitmap. See mbitmap.go for details.
    // gcdata存储着GC类型数据
    gcdata    *byte
    // 类型名字的偏移
	str       nameOff
	ptrToThis typeOff
}
```
_type是go所有类型的公共描述，里面包含GC，反射等需要的细节，它决定data应该如何解释和操作，在别的结构中也可以看到_type这个结构体

## iface
iface结构体表示非空的接口

```go
// runtime/runtime2
type iface struct {
	tab  *itab // 接口的类型以及赋给这个接口的试题类型
	data unsafe.Pointer
}
```
data是指向数据的指针  
itab是非空接口的类型信息  
`itab`的结构
```go
type itab struct {
    // 接口的类型
    inter *interfacetype
    // 实体的类型
    _type *_type
	hash  uint32 // copy of _type.hash. Used for type switches.
    _     [4]byte
    
    // 存放接口方法对应的具体数据类型和方法地址
	fun   [1]uintptr // variable sized. fun[0]==0 means _type does not implement inter.
}

```
接口类型信息的实现
```go
type imethod struct {
	name nameOff
	ityp typeOff
}

type interfacetype struct {
	typ     _type
	pkgpath name
	mhdr    []imethod
}
```

fun表示interface里面的方法的具体实现。 但是可以看到fun的长度是1，fun只存储接口中定义的按照字典序的第一个方法的地址，后续的方法的地址是连续的，寻找的时候按照内存地址连续就可以找到 
使用测试程序测试下这个多个`method`
```go
package main

type MyInterface interface {
	Print()
	Hello()
	Word()
	AWK()
}

func Foo(me MyInterface) {
	me.Print()
	me.Hello()
	me.Word()
	me.AWK()
}

type MyStruct struct{}

func(ms MyStruct)Print(){}
func(ms MyStruct)Hello(){}
func(ms MyStruct)Word(){}
func(ms MyStruct)AWK(){}

func main() {
	var me MyStruct
	Foo(me)
}

```

```shell
➜  go build --gcflags '-l' -o fun fun.go //编译
➜  go tool objdump -s "main\.Foo" fun 
TEXT main.Foo(SB) /Users/wanglitao/go/src/awesomeProject1/interface/fun.go
  fun.go:10             0x104e140               65488b0c2530000000      MOVQ GS:0x30, CX                        
  fun.go:10             0x104e149               483b6110                CMPQ 0x10(CX), SP                       
  fun.go:10             0x104e14d               7668                    JBE 0x104e1b7                           
  fun.go:10             0x104e14f               4883ec10                SUBQ $0x10, SP                          
  fun.go:10             0x104e153               48896c2408              MOVQ BP, 0x8(SP)                        
  fun.go:10             0x104e158               488d6c2408              LEAQ 0x8(SP), BP                        
  fun.go:11             0x104e15d               488b442418              MOVQ 0x18(SP), AX       // 代表itab的地址               
  fun.go:11             0x104e162               488b4828                MOVQ 0x28(AX), CX       // 取出Print函数地址  
  fun.go:11             0x104e166               488b542420              MOVQ 0x20(SP), DX                       
  fun.go:11             0x104e16b               48891424                MOVQ DX, 0(SP)                          
  fun.go:11             0x104e16f               ffd1                    CALL CX                 // 调用Print()                        
  fun.go:12             0x104e171               488b442418              MOVQ 0x18(SP), AX                       
  fun.go:12             0x104e176               488b4820                MOVQ 0x20(AX), CX       // 取出Hello函数地址                 
  fun.go:12             0x104e17a               488b542420              MOVQ 0x20(SP), DX                       
  fun.go:12             0x104e17f               48891424                MOVQ DX, 0(SP)                          
  fun.go:12             0x104e183               ffd1                    CALL CX                 // 调用Hello()                          
  fun.go:13             0x104e185               488b442418              MOVQ 0x18(SP), AX                       
  fun.go:13             0x104e18a               488b4830                MOVQ 0x30(AX), CX       // 取出Word函数地址                 
  fun.go:13             0x104e18e               488b542420              MOVQ 0x20(SP), DX                       
  fun.go:13             0x104e193               48891424                MOVQ DX, 0(SP)                          
  fun.go:13             0x104e197               ffd1                    CALL CX                 // 调用Word()                
  fun.go:14             0x104e199               488b442418              MOVQ 0x18(SP), AX                       
  fun.go:14             0x104e19e               488b4018                MOVQ 0x18(AX), AX     // 取出AWK函数地址        
  fun.go:14             0x104e1a2               488b4c2420              MOVQ 0x20(SP), CX                       
  fun.go:14             0x104e1a7               48890c24                MOVQ CX, 0(SP)                          
  fun.go:14             0x104e1ab               ffd0                    CALL AX                 // 调用AWK()                
  fun.go:15             0x104e1ad               488b6c2408              MOVQ 0x8(SP), BP                        
  fun.go:15             0x104e1b2               4883c410                ADDQ $0x10, SP                          
  fun.go:15             0x104e1b6               c3                      RET                                     
  fun.go:10             0x104e1b7               e82489ffff              CALL runtime.morestack_noctxt(SB)       
  fun.go:10             0x104e1bc               eb82                    JMP main.Foo(SB)                        
  :-1                   0x104e1be               cc                      INT $0x3                                
  :-1                   0x104e1bf               cc                      INT $0x3                                
➜
```
每个方法的位置是按照字典序排列在内存中
`AWK`的地址是`0x18(AX)`,`Hello`的内存地址`0x20(AX)`，`Print`的地址是`0x28(AX)`，`Word`的地址是`0x30(AX)`，依照这个顺序就可以取出所有的方法了


## 接口的动态类型和动态值
iface包含两部分:`tab`指向类型信息，`data`指向具体的数据。

- 接口类型与`nil`比较
接口值的零值是指`动态类型`和`动态值`都为`nil`。否则这个接口类型是与`nil`不相等的
EG:
```go
package main

import "fmt"

type Coder interface {
	code()
}

type Gopher struct {
	name string
}

func (g Gopher) code() {
	fmt.Printf("%s is coding\n", g.name)
}

func main() {
	var c Coder
	fmt.Println(c == nil) // true
	fmt.Printf("c: %T, %v\n", c, c)

	var g *Gopher
	fmt.Println(g == nil) // true

	c = g
	fmt.Println(c == nil) // false
	fmt.Printf("c: %T, %v\n", c, c)
}
```
将`g`赋给`c`的时候，`c`的动态类型就不为`nil`了，所以就不等于`nil`了