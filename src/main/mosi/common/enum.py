#!/usr/bin/env python
from enum import Enum as _Enum, IntEnum as _IntEnum

from .exceptions import raise_enum_error as _raise_enum_error


# noinspection PyClassHasNoInit
class BaseEnum(_Enum):

    @classmethod
    def parse(cls, enum):
        try:
            return cls(enum)
        except ValueError:
            if isinstance(enum, str) and enum.upper() in cls.__members__:
                return cls.__members__[enum.upper()]
            else:
                _raise_enum_error(cls, enum)


# noinspection PyUnresolvedReferences
class BaseIntEnum(_IntEnum):

    @classmethod
    def parse(cls, enum):
        try:
            return cls(int(enum))
        except ValueError:
            if isinstance(enum, str) and enum.upper() in cls.__members__:
                return cls.__members__[enum.upper()]
            else:
                raise_enum_error(cls, enum)


# noinspection PyClassHasNoInit
class ConstraintType(BaseEnum):
    EQ = "eq"
    LE = "le"
    GE = "ge"
    __INV__ = {EQ: EQ, GE: LE, LE: GE}
    __LP__ = {EQ: "=", GE: ">=", LE: "<="}
    __MPS__ = {EQ: "E", GE: "G", LE: "L"}

    def __invert__(self):
        return ConstraintType(self.__INV__[self.value])

    def to_lp(self):
        return self.__LP__[self.value]

    def to_mps(self):
        return self.__MPS__[self.value]


class ModelStatus(BaseIntEnum):
    OPTIMAL = 1
    UNSOLVED = 0
    INFEASIBLE = -1
    UNBOUND = -2
    UNDEFINED = -3

    def is_solved(self):
        return self.value > 0


# noinspection PyClassHasNoInit
class ObjectiveType(BaseEnum):
    MIN = "min"
    MAX = "max"
    __INV__ = {MIN: MAX, MAX: MIN}
    __LP__ = {MIN: "MINIMIZE", MAX: "MAXIMIZE"}
    __MPS__ = {MIN: "MIN", MAX: "MAX"}

    def __invert__(self):
        return ObjectiveType(self.__INV__[self.value])

    def to_lp(self):
        return self.__LP__[self.value]

    def to_mps(self):
        return self.__MPS__[self.value]


# noinspection PyClassHasNoInit
class VariableType(BaseEnum):
    FLOAT = "float"
    BINARY = "binary"
    INTEGER = "integer"
    SEMI_CONTINUOUS = "semi-continuous"
    SEMI_INTEGER = "semi-integer"
    __FLOAT__ = {FLOAT, SEMI_CONTINUOUS}
    __INTEGER__ = {BINARY, INTEGER, SEMI_CONTINUOUS, SEMI_INTEGER}

    def get_parser(self):
        if self.value in self.__FLOAT__:
            return lambda value: float(value)
        else:
            return lambda value: round(float(value))
