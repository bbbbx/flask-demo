'''
Python 调用 C 语言例子
https://python3-cookbook.readthedocs.io/zh_CN/latest/chapters/p15_c_extensions.html

    >>> import sample
    >>> sample.gcd(35, 7)
    7
    >>> sample.divide(42, 8)
    (5, 2)

'''

import ctypes
import os

_file = 'libsample.so'
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
_mod = ctypes.cdll.LoadLibrary(_path)

# int gcd(int, int)
gcd = _mod.gcd
gcd.argtypes = (ctypes.c_int, ctypes.c_int)
gcd.restype = ctypes.c_int

# int divide(int, int, int*)
_divide = _mod.divide
_divide.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_int))
_divide.restype = ctypes.c_int

def divide(x, y):
    rem = ctypes.c_int()
    quot = _divide(x, y, rem)
    return quot, rem.value

calc_pi = _mod.calc_pi
calc_pi.argtypes = [ctypes.c_int]
calc_pi.restype = ctypes.c_double
