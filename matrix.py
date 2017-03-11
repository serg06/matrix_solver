try:
    from row import Row, LenMismatchError
except ImportError:
    from .row import Row, LenMismatchError


class Matrix(list):
    def __init__(self, seq=()):
        super().__init__()
        self.rowlen = 0
        for row in seq:
            self.append(row)

    # append row
    def append(self, row):
        if len(self) == 0:
            self.rowlen = len(row)
        elif len(row) != self.rowlen:
            raise LenMismatchError()

        super().append(Row(row))

    # swap 2 rows
    def swap(self, i1: int, i2: int):
        if i1 == i2:
            return
        temp = self[i1]
        self[i1] = self[i2]
        self[i2] = temp

    # perform gauss-jordan elimination on the matrix
    def gauss_jordan(self):
        finished_rows = 0
        for coli in range(self.rowlen):
            # find unfinished row with leading 0s and a number at coli
            for rowi in range(finished_rows, len(self)):
                # if non-0 at col-i and leading 0s
                if self[rowi][coli] != 0 and coli == self[rowi][0:coli].count(0):
                    # row reduce
                    self[rowi].row_reduce()
                    # subtract from other rows as needed
                    self._gauss_subtract(rowi, coli)
                    self.swap(rowi, finished_rows)
                    finished_rows += 1

            if finished_rows == len(self):
                break

    # subtract given row from every other row so that it is the only non-0 item in the column
    def _gauss_subtract(self, the_rowi: int, the_coli: int):
        for rowi in range(len(self)):
            # skip given row
            if rowi == the_rowi:
                continue
            scale_by = self[rowi][the_coli]
            self[rowi] = self[rowi] - (self[the_rowi] * scale_by)

    def __mul__(self, other):
        if self.rowlen != len(other):
            raise LenMismatchError("Error: A's row lengths and B's column lengths don't match.")

        if len(self) == 0:
            return self

        return Matrix(
            # resulting matrix
            [
                # each row of resulting matrix
                [
                    # each entry of row
                    sum([
                        # each product of A & B
                        self[A_row_index][matching_index] * other[matching_index][B_col_index]

                        # for each matching col in A & row in B
                        for matching_index in range(self.rowlen)
                    ])

                    # for each column in B
                    for B_col_index in range(other.rowlen)
                ]

                # for each row in A
                for A_row_index in range(len(self))
            ]
        )

    def __str__(self):
        result = ''
        if len(self) == 0 or self.rowlen == 0:
            result = '[]\n'
        for row in self:
            result += str(row) + '\n'
        return result[:-1]
