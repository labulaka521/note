## reflect 

reflect.Type 表示 interface{} 的具体类型 main.order
reflect.Value 表示它的具体值。
reflect.TypeOf() 和 reflect.ValueOf() 两个函数可以分别返回 reflect.Type 和 reflect.Value。


relfect.Kind 表示该类型的特定类别 struct

NumField() 方法返回结构体中字段的数量，而 Field(i int) 方法返回字段 i 的 reflect.Value。

Int 和 String 可以帮助我们分别取出 reflect.Value 作为 int64 和 string。

tag

```

const tagName = "validate"

type User struct {
	Id int `validate:"-"`
	Name string `validate:"presence,min=2,max=23"`
	Email string `validate:"email,required"`
}

func main() {
	user := User{
		Id: 1,
		Name: "wang",
		Email: "wang@li.tao",
	}
	t := reflect.TypeOf(user)

	fmt.Println(t.Kind(), t.Name(), t.NumField())
	for i := 0;i < t.NumField(); i++ {
		field := t.Field(i)
		tag := field.Tag.Get(tagName)
		fmt.Println(field.Name ,field.Type.Name(), tag)
	}
}
```