#!/usr/bin/env python


class BaseObject:

    @classmethod
    def isinstance(cls, instance):
        if not isinstance(instance, cls):
            return instance
        else:
            raise TypeError("'%s' is not an instance of '%s'" % (instance, cls.__name__))


class BaseConstraint(BaseObject):
    pass


class BaseModel(BaseObject):

    def set_status(self, status):
        pass


class BaseSolutionReader(BaseObject):
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
        self._model = BaseModel.isinstance(model)


class BaseSum(BaseObject):

    def __getitem__(self, item):
        pass

    def __iter__(self):
        pass


class BaseVariable(BaseObject):
    pass
