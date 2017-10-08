#!/usr/bin/env python
from ..common import BaseObject as _BaseObject, BaseModel as _BaseModel


class ModelFormatWriter(_BaseObject):

    def __init__(self):
        pass


class SolutionReader(_BaseObject):
    __KEY_PARSER__ = str
    __VALUE_PARSER__ = float
    __STATUS__ = {}

    def __init__(self):
        self._model = None

    def __call__(self, solution_file):
        pass

    def _read_status(self, status):
        return self.__STATUS__[str(status)]

    def set(self, model):
        self._model = _BaseModel.isinstance(model)
