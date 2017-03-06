from fractions import Fraction


class Row(list):
    def __init__(self, seq=()):
        super().__init__(Fraction(x) for x in seq)

    def row_reduce(self):
        if self == [0 for x in self]:
            return
        divide_amt = [x for x in self if x != 0][0]
        new = self / divide_amt
        for i in range(len(new)):
            self[i] = new[i]

    def __mul__(self, other):
        return Row(map(lambda x: x * other, self))

    def __truediv__(self, other):
        return Row(map(lambda x: x / other, self))

    def __add__(self, other):
        if len(self) != len(other):
            raise LenMismatchError()
        return Row(self[i] + other[i] for i in range(len(self)))

    def __sub__(self, other):
        if len(self) != len(other):
            raise LenMismatchError()
        return Row(self[i] - other[i] for i in range(len(self)))

    def __str__(self):
        def int_or_float(x):
            if x == int(x):
                return int(x)
            else:
                return float(x)
        return str([int_or_float(x) for x in self])


class LenMismatchError(Exception):
    def __init__(self, message="Error: Row lengths don't match."):
        self.message = message
