from fractions import Fraction

# decimals to round to
round_to = 3


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
        global round_to

        # convert fraction to int or float, depending on whether it has decimals
        def to_readable_float(x):
            if x == int(x):
                return int(x)
            else:
                return float("%.{}f".format(round_to) % float(x))

        # convert fraction to int or readable fraction (num/den)
        def to_readable_fraction(x):
            if x == int(x):
                return int(x)
            else:
                return "{}/{}".format(x.numerator, x.denominator)

        return str([to_readable_fraction(x) for x in self]).replace("'","")


class LenMismatchError(Exception):
    def __init__(self, message="Error: Row lengths don't match."):
        self.message = message
