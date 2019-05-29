##__init__##  
__init__通常在初始化一个实例的时候使用
控制这个初始化的过程   
实例级别的方法  

##__new__##  
__new__方式是创建这个实例的方法  
主要适当继承一些不可变的类时(int, str)，提供一个自定义这些类的实例化的过程


```
# 创建实例
class Persion:
    def __new__(cls, name, age):
        print('running __new__ called')
        return super(Persion, cls).__new__(cls)

    def __init__(self, name, age):
        print('run __init__ called')
        self.name = name
        self.age = age

    def __str__(self):
        return f'<Persion: {self.name}({self.age})'
p = Persion('wang', 21)
print(p)
```

- 继承int类型  
```
class PositiveInteger(int):

    # def __init__(self, value):
    #     super().__init__(self, abs(value))

    def __new__(cls, value):
        return super(PositiveInteger, cls).__new__(cls, abs(value))


i = PositiveInteger(-3)
print(i)
```

 还可以使用`__new__`来实现一个单例模式  

 ```
 #  实现单例模式
class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance

obj1 = Singleton()
obj2 = Singleton()

obj1.test = 'lalalal'

print(obj1.test, obj2.test)
print(obj1 is obj2)
```
