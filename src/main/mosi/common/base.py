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


class BaseSum(BaseObject):

    def __getitem__(self, item):
        pass

    def __iter__(self):
        pass


class BaseVariable(BaseObject):
    pass
