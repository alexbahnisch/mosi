#!/usr/bin/env python


def make_dict(cls, *keyss, **kwargs):
    if len(keyss) == 0:
        return cls(**kwargs)
    else:
        rv = {}
        keys, *keyss = keyss
        name = kwargs.pop("name")
        for key in keyss[0]:
            if name is not None:
                rv[key] = make_dict(cls, *keyss, name="%s_%s" % (name, key), **kwargs)
            else:
                rv[key] = make_dict(cls, *keyss, **kwargs)
        return rv


def make_list(cls, *dimensions, **kwargs):
    if len(dimensions) == 0:
        return cls(**kwargs)
    else:
        rv = []
        dimension, *dimensions = dimensions
        name = kwargs.pop("name")
        for index in range(dimension):
            if name is not None:
                rv.append(make_list(cls, *dimensions, name="%s_%s" % (name, index), **kwargs))
            else:
                rv.append(make_list(cls, *dimensions, **kwargs))
        return rv


def _make_tuple_dict(cls, tup, *keyss, **kwargs):
    if len(keyss) == 0:
        return cls(**kwargs)
    else:
        rv = {}
        keys, *keyss = keyss
        name = kwargs.pop("name")

        for key in keyss[0]:
            temp_tup = (*tup, key)
            if name is not None:
                rv.update(_make_tuple_dict(cls, temp_tup, *keyss, name="%s_%s" % (name, key), **kwargs))
            else:
                rv.update(_make_tuple_dict(cls, temp_tup, *keyss, **kwargs))
        return rv


def make_tuple_dict(cls, name, *keyss, **kwargs):
    return _make_tuple_dict(cls, name, (), *keyss, **kwargs)
