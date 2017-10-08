#!/usr/bin/env python
from mosi.common.base import *
from pytest import raises


def test_base_object():
    obj = BaseObject()
    assert obj == BaseObject.isinstance(obj)


def test_base_object_exception():
    with raises(TypeError, message="'object' is not an instance of 'BaseObject'"):
        BaseObject.isinstance(object())
