接口对象由接口表(interface table)指针和数据指针组成

```
struct Iface
{
    Itab* tab;
    void*    data;
};

struct Itab {
    InterfaceType*    inter;
    Type*             type;
    void (*fun[])(void);
};
```
接口表存储元数据信息，包括接口类型 动态类型 以及实现接口的方法指针。无论是反射还是通过接口调用方法，都会用到这些信息

数据指针持有的是目标对象的只读复制品，复制完整对象或指针。


只有在tab和data都为nil时，接口才等于nil

