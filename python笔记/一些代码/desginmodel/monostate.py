# 赋值给__init__
class Borg:
    __share_state = {"1": "2"}

    def __init__(self):
        self.__dict__ = self.__share_state
        self.__dict__['x'] = 1


b = Borg()
b1 = Borg()

print(b, b1)
b.__dict__['y'] = 1
print(b.__dict__, b1.__dict__)


# class Borg_new:
#     _share_state = {}
# def __new__(cls, *args, **kwargs):
#         obj = super(Borg_new, cls).__new__(cls, *args, **kwargs)
#         obj.__dict__ = cls._share_state
#         return obj



class Borg_n:
    _share_state = {}
    def __new__(cls, *args, **kwargs):
        obj = super(Borg_n, cls).__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._share_state
        return obj

bn = Borg_n()
bn.__dict__['x'] =1
bn1 = Borg_n()
print(bn.__dict__)
print(bn1.__dict__)
