`__call__` 可以多次调用  
```
>>> class x:
...     def __init__(self,a):
...         self.a = a
...     def __call__(self,b):
...         self.b = b
...         print(self,b)
...
>>> A=x(1)
>>> A
<__main__.x object at 0x101f07be0>
>>> A(2)
<__main__.x object at 0x101f07be0> 2
>>> A(13)
<__main__.x object at 0x101f07be0> 13
```

- new： 对象的创建，是一个静态方法，第一个参数是cls。(想想也是，不可能是self，对象还没创建，哪来的self)  
- init ： 对象的初始化， 是一个实例方法，第一个参数是self。  
- call ： 对象可call，注意不是类，是对象。


使用普通类的时候需要先实例化一个调用对象再调用方法
而使用@staticmethod或@classmethod，就可以不需要实例化，直接类名.方法名()来调用。

这有利于组织代码，把某些应该属于某个类的函数给放到那个类里去，同时有利于命名空间的整洁。


既然@staticmethod和@classmethod都可以直接类名.方法名()来调用，那他们有什么区别呢

从它们的使用上来看,


@staticmethod不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样。
@classmethod也不需要self参数，但第一个参数需要是表示自身类的cls参数。
如果在@staticmethod中要调用到这个类的一些属性方法，只能直接类名.属性名或类名.方法名。

而@classmethod因为持有cls参数，可以来调用类的属性，类的方法，实例化对象等，避免硬编码。

class A(object):
    bar = 1

    def foo(self):
        print('foo')

    @staticmethod
    def static_foo():
        print('static_foo')
        print(A.bar)

    @classmethod
    def class_foo(cls):
        print('class_foo')
        print(cls.bar)
        cls().foo()


A.static_foo()
A.class_foo()




property 将一个方法变成属性调用  
```
class Student:
    @property
    def score(self):
        return self._value

    @score.setter
    将方法变成可以赋值的。
    def score(self, value):
        self._value = value
```
```
>>> from property import Student
>>> s = Student()
>>> s.score
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/admin/python/property.py", line 4, in score
    return self._value
AttributeError: 'Student' object has no attribute '_value'
>>> s.score = 1
>>> s.score
1
```
