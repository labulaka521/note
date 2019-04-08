class Student:
    @property
    def score(self):
        return self._value

    @score.setter
    def score(self, value):
        self._value = value



