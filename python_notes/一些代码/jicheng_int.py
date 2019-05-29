class PositiveInteger(int):

    # def __init__(self, value):
    #     super().__init__(self, abs(value))

    def __new__(cls, value):
        return super(PositiveInteger, cls).__new__(cls, abs(value))


i = PositiveInteger(-3)
print(i)



