class Persion:
    def __new__(cls, name, age):
        print('running __new__ called')
        return super(Persion, cls).__new__(cls)

    # def __new__(cls, name, age):
    #     obj = str.__new

    def __init__(self, name, age):
        print('run __init__ called')
        self.name = name
        self.age = age

    def __str__(self):
        return f'<Persion: {self.name}({self.age})'
p = Persion('wang', 21)
print(p)
