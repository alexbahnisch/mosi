#!/usr/bin/env python
from copy import copy

from .base import BaseSum, BaseVariable


class CoefficientMap(dict):

    def __init__(self):
        super().__init__([])

    def __getitem__(self, item):
        if item not in self:
            self[item] = float()
        return super().__getitem__(item)

    def __add__(self, other):
        if isinstance(other, (BaseSum, CoefficientMap)):
            for key in other:
                self[key] += float(other[key])
            return self
        elif isinstance(other, BaseVariable):
            self[other] += 1
            return self
        elif isinstance(other, dict):
            for key in other:
                self[BaseVariable.isinstance(key)] += float(other[key])
            return self
        else:
            # TODO - raise better exception
            raise Exception("TODO - raise better exception")

    def __sub__(self, other):
        if isinstance(other, (BaseSum, CoefficientMap)):
            for key in other:
                self[key] -= float(other[key])
            return self
        elif isinstance(other, BaseVariable):
            self[other] -= 1
            return self
        elif isinstance(other, dict):
            for key in other:
                self[BaseVariable.isinstance(key)] -= float(other[key])
            return self
        else:
            # TODO - raise better exception
            raise Exception("TODO - raise better exception")

    @classmethod
    def parse(cls, dictionary):
        if isinstance(dictionary, CoefficientMap):
            return copy(dictionary)
        elif isinstance(dictionary, dict):
            instance = cls()
            for key in dictionary:
                instance[BaseVariable.isinstance(key)] += float(dictionary[key])
            return instance
        else:
            # TODO - raise better exception
            raise Exception("TODO - raise better exception")
