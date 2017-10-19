#!/usr/bin/env python
from pyplus.singleton import Singleton as _Singleton

from .base import BaseObject as _BaseObject


# noinspection PyClassHasNoInit
class NoValueType(_BaseObject, metaclass=_Singleton):

    def __abs__(self):
        return self

    def __bool__(self):
        return False

    def __ceil__(self):
        return self

    def __round__(self, n=None):
        return self

    def __floor__(self):
        return self

    def __pos__(self):
        return self

    def __neg__(self):
        return self

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __ge__(self, other):
        return False

    def __gt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __add__(self, other):
        return self

    def __iadd__(self, other):
        return self

    def __radd__(self, other):
        return self

    def __sub__(self, other):
        return self

    def __isub__(self, other):
        return self

    def __rsub__(self, other):
        return self

    def __mul__(self, other):
        return self

    def __imul__(self, other):
        return self

    def __rmul__(self, other):
        return self

    def __truediv__(self, other):
        return self

    def __idiv__(self, other):
        return self

    def __rdiv__(self, other):
        return self

    def __pow__(self, power, modulo=None):
        return self

    def __floordiv__(self, other):
        return self

    def __mod__(self, other):
        return self

    def __divmod__(self, other):
        return self, self

    def __repr__(self):
        return "NoValue"

    def __str__(self):
        return "NoValue"

NoValue = NoValueType()
