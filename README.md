# Matrix solver
A python3 matrix solver. Currently only supported matrix transformation is gauss-jordan elimination. May expand later.

Example command-line usage:
```
$ git clone git@github.com:serg06/matrix_solver.git
$ python3
Python 3.4.5 (default, Oct 10 2016, 14:41:48)
[GCC 5.4.0] on cygwin
Type "help", "copyright", "credits" or "license" for more information.
>>> from matrix_solver.matrix import Matrix
>>>
>>> m = Matrix(
...     [
...         [1, 1, 2, 0, 1],
...         [2, -1, 0, 1, -2],
...         [1, -1, -1, -2, 4],
...         [2, -1, 2, -1, 0]
...     ]
... )
>>>
>>> print(m)
[1, 1, 2, 0, 1]
[2, -1, 0, 1, -2]
[1, -1, -1, -2, 4]
[2, -1, 2, -1, 0]
>>>
>>> m.gauss_jordan()
>>>
>>> print(m)
[1, 0, 0, 0, 1]
[0, 1, 0, 0, 2]
[0, 0, 1, 0, -1]
[0, 0, 0, 1, -2]
>>>
```
