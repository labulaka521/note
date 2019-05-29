
自动增长
```
const (
    CategoryBooks = iota // 0
    CategoryHealth       // 1
    CategoryClothing     // 2
)
```

使用下划线跳过不需要的值
```
const (
    CategoryBooks = iota // 0
    CategoryHealth       // 1
    CategoryClothing     // 2
)
```

表达式 位运算
竖线与运算得到两个二进制数共同拥有的位
```
type Allergen int

const (
    IgEggs Allergen = 1 << iota         // 1 << 0 左移一位 00000001     1
    IgChocolate                         // 1 << 1 左移两位 is 00000010  2
    IgNuts                              // 1 << 2 左移三位 is 00000100  4
    IgStrawberries                      // 1 << 3 左移四位 is 00001000  8
    IgShellfish                         // 1 << 4 左移五位 is 00010000  18
)

fmt.Println(IgEggs | IgChocolate | IgShellfish) //00010011 19

fmt.Println(2 | 3) // 00000010 | 00000011 -> 00000011 3
```

容量大小的表示
```
type ByteSize int
const (
    _             = iota  // 将0值忽略
    KB   ByteSize = 1 << ( 10 * iota )  // 1 << (10 * 1)  1024
    MB                                  // 1 << (10 * 2) 
    GB                                  // 1 << (10 * 3)
    TB                                  // 2 << (10 8 4)
)
```
提供多组iota
```
	const (
		A, B = iota, iota << 10	//0 0 << 10
		C, D			//1 1 << 10
	)
```
被打断需要显示恢复
```
	const (
		A1 =iota
		B1
		C1 = "a"
		D1
		E1
	)
	fmt.Println(B1,D1)
```

简单的位运算演示
```
0110 & 1011 = 0010 AND的关系
0110 | 1011 = 1111 OR
0110 ^ 1011 = 1101 只能为一个
0110 &^ 1011 = 0100 清除后面的标志位
```

[play](https://play.studygolang.com/p/fx3f2UhwNAb)