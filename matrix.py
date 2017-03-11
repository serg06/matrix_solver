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

        return self

    # subtract given row from every other row so that it is the only non-0 item in the column
    def _gauss_subtract(self, the_rowi: int, the_coli: int):
        for rowi in range(len(self)):
            # skip given row
            if rowi == the_rowi:
                continue
            scale_by = self[rowi][the_coli]
            self[rowi] = self[rowi] - (self[the_rowi] * scale_by)

    def inverse(self):
        if len(self) != self.rowlen:
            raise LenMismatchError("Error: Cannot invert matrix with different row and column lengths.")

        self._append_right_identity()
        self.gauss_jordan()
        self._delete_left_identity()

        return self

    def _append_right_identity(self):
        # extend matrix with identity equivalent on the right
        for row_num, row in enumerate(self):
            row.extend([0 if col_num != row_num else 1 for col_num in range(self.rowlen)])

        self.rowlen *= 2

    def _delete_left_identity(self):
        # remove identity half (on the left)
        self.rowlen = int(self.rowlen/2)

        for row_num, row in enumerate(self):
            for col_num in range(self.rowlen):
                row.pop(0)

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

    def copy(self):
        return Matrix(super().copy())
