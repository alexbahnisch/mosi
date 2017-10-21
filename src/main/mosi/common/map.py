#!/usr/bin/env python
from collections import defaultdict

from .base import BaseSum, BaseVariable


class CoefficientMap(defaultdict):

    def __init__(self):
        super().__init__(float)

    def __add__(self, other):
        if isinstance(other, (BaseSum, CoefficientMap)):
            for key in other:
                self[key] += float(other[key])
            return self
        elif isinstance(other, dict):
            for key in other:
                self[BaseVariable.isinstance(key)] += float(other[key])
            return self
        else:
            # TODO - raise better exception
            raise Exception("TODO - raise better exception - fnbvskjfeifhseknfe")

    def __sub__(self, other):
        if isinstance(other, (BaseSum, CoefficientMap)):
            for key in other:
                self[key] -= float(other[key])
            return self
        elif isinstance(other, dict):
            for key in other:
                self[BaseVariable.isinstance(key)] -= float(other[key])
            return self
        else:
            # TODO - raise better exception
            raise Exception("TODO - raise better exception - dasjfevheasdjegvtg")

    @classmethod
    def new(cls, dictionary):
        if isinstance(dictionary, CoefficientMap):
            return dictionary
        elif isinstance(dictionary, dict):
            instance = cls()
            for key in dictionary:
                instance[BaseVariable.isinstance(key)] += float(dictionary[key])
            return instance
        else:
            # TODO - raise better exception
            raise Exception("TODO - raise better exception - fdsajdgfdgsfshfju")
