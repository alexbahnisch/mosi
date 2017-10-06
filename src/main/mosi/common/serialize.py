#!/usr/bin/env python
from functools import wraps as _wraps

from pyplus.common import isintlike as _isintlike, isnumber as _isnumber

from ._objects import BaseObject as _BaseObject


def _parse(method):
    @_wraps(method)
    def wrapped(self, string):
        if isinstance(string, str):
            return method(self, string)
        else:
            raise TypeError("%s() argument must be a 'str', not '%s'" % (method.__name__, type(string).__name__))

    return wrapped


class IndexSerializer(_BaseObject):
    __LOWER__ = [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
        'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]

    def __init__(self, length=7, capitals=True):
        if _isintlike(length):
            length = int(length)
            if length > 0:
                self._length = length
                self._limit = self.__BASE__ ** length
                self._characters = self.__UPPER__ if capitals else self.__LOWER__
                if length > 1:
                    self._sub_serializer = IndexSerializer(length - 1, capitals)
                else:
                    self._sub_serializer = None
            else:
                raise ValueError("'length' argument must be greater than 0")
        else:
            raise TypeError("'length' argument must be an 'int' like object not '%s'" % int(length).__name__)

    @property
    def __BASE__(self):
        return len(self.__LOWER__)

    @property
    def __UPPER__(self):
        return [char.upper() for char in self.__LOWER__]

    @_parse
    def parse(self, string):
        if len(string) == self._length:
            rarg = 0
            for index, character in enumerate(reversed(string)):
                try:
                    rarg += self._characters.index(character) * (self.__BASE__ ** index)
                except ValueError:
                    raise ValueError(
                        "'%s' is an invalid character for this instance of a '%s'" % (character, type(self).__name__))
            return rarg
        else:
            raise ValueError("parse() argument must have '%s' characters" % self._length)

    def serialize(self, index):
        if _isintlike(index):
            index = int(index)
            if 0 <= index < self._limit:
                if self._sub_serializer:
                    div, mod = divmod(int(index), self.__BASE__)
                    return self._sub_serializer.serialize(div) + self._characters[mod]
                else:
                    return self._characters[index]
            else:
                raise ValueError("serialize() 'index' argument must be between 0 and %s" % self._limit)
        else:
            raise TypeError("serialize() 'index' argument must be an 'int' like object not '%s'" % type(self).__name__)


class NumberSerializer(_BaseObject):
    __MAX__ = 10 ** 100
    __MIN__ = 10 ** -100

    def __init__(self, length=12, capitals=True, tolerance=10 ** -10):
        if _isintlike(length):
            length = int(length)
            if length > 8:
                self._big_exp_format = "%+." + str(length - 8) + ("E" if bool(capitals) else "e")
                self._exp_format = "%+." + str(length - 7) + ("E" if bool(capitals) else "e")
                self._float_format = "%+." + str(length) + "f"
                self._float_min = 10 ** - 3
                self._float_max = 10 ** (length - 1)
                self._string_format = "%" + str(length) + "." + str(length) + "s"
                self._tolerance = float(tolerance)
                self._zero = " " * (length - 2) + "+0"

            else:
                raise ValueError("'length' argument must be greater than 0")

        else:
            raise TypeError("'length' argument must be an 'int' like object not '%s'" % int(length).__name__)

    @_parse
    def parse(self, string):
        return float(string)

    def serialize(self, number):
        if _isnumber(number):
            abs_number = abs(number)
            if abs_number <= self._tolerance:
                return self._zero
            elif self._float_min < abs_number < self._float_max:
                return self._string_format % (self._float_format % float(number))
            elif self.__MIN__ < abs_number < self.__MAX__:
                return self._exp_format % float(number)
            else:
                return self._big_exp_format % float(number)
        else:
            raise TypeError("serialize() 'number' argument must be an number like object not '%s'" % type(self).__name__)

