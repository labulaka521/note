单引号字符常量表⽰示 Unicode Code Point，⽀支持 \uFFFF、\U7FFFFFFF、\xFF 格式。 对应 rune 类型，UCS-4。

修改字符串可将其现转换成[]rune 或者[]byte 完成后在转换为string 无论哪种转 换，都会重新分配内存，并复制字节数组。

```
	a := "abcd"
	bs := []byte(a)
	bs[0] = 'A'
	fmt.Println(string(bs))
	
	fmt.Printf("%T\n", 's')
	
	a1 := "王丽涛"
	a1u := []rune(a1)
	a1u[1] = '网'
	fmt.Println(string(a1u))

    // for循环便利字符串时 byte 和rune两种方式
    s := "abc汉字"
	for i := 0; i < len(s); i++ {
		fmt.Printf("%c,", s[i])
	}
	fmt.Println()
	for _, r := range s {
		fmt.Printf("%c,", r)
	}
```

- 既然string就是一系列字节，而[]byte也可以表达一系列字节，那么实际运用中应当如何取舍？
- string可以直接比较，而[]byte不可以，所以[]byte不可以当map的key值。
- 因为无法修改string中的某个字符，需要粒度小到操作一个字符时，用[]byte。
- string值不可为nil，所以如果你想要通过返回nil表达额外的含义，就用[]byte。
- []byte切片这么灵活，想要用切片的特性就用[]byte。
- 需要大量字符串处理的时候用[]byte，性能好很多。