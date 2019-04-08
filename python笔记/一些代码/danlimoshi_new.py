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
