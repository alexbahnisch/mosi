#!/usr/bin/env python


class BaseObject:

    @classmethod
    def isinstance(cls, instance):
        if isinstance(instance, cls):
            return instance
        else:
            raise TypeError("'%s' is not an instance of '%s'" % (type(instance).__name__, cls.__name__))

    @classmethod
    def issubclass(cls, clazz):
        try:
            if issubclass(clazz, cls):
                return clazz
            else:
                raise TypeError("'%s' is not an subclass of '%s'" % (clazz.__name__, cls.__name__))
        except TypeError:
            raise TypeError("instance of '%s' is not an subclass of '%s'" % (type(clazz).__name__, cls.__name__))


class BaseConstraint(BaseObject):
    pass


class BaseModel(BaseObject):

    def get_name(self):
        pass

    def set_status(self, status):
        pass


class BaseSum(BaseObject):

    def __getitem__(self, item):
        pass

    def __iter__(self):
        pass


class BaseVariable(BaseObject):
    pass
