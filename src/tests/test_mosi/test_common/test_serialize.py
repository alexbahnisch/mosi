#!/usr/bin/env python
from random import randint, random

from mosi.common import IndexSerializer, NumberSerializer
from pytest import raises


def assert_number(number, parsed, magnitude=-5):
    assert abs(parsed / number) - 1 <= 10 ** magnitude


def random_number(magnitude):
    return (1 if randint(0, 1) else -1) * random() * 10 ** ((1 if randint(0, 1) else -1) * randint(0, magnitude))


def test_index_serialize():
    serials = []
    serializer = IndexSerializer(length=7, capitals=True)

    for number in range(0, 49000, 49):
        serial = serializer.serialize(number)
        assert number == serializer.parse(serial)
        assert serial not in serials
        serials.append(serial)


def test_index_serializer_exceptions():
    serializer = IndexSerializer(length=7, capitals=True)

    with raises(TypeError, message="'length' argument must be an 'int' like object not 'object'"):
        IndexSerializer(length=object())

    with raises(ValueError, message="'length' argument must be greater than 0"):
        IndexSerializer(length=0)

    with raises(TypeError, message="parse() argument must be a 'str', not 'object'"):
        serializer.parse(object())

    with raises(ValueError, message="parse() argument must have '7' characters"):
        serializer.parse("0000")

    with raises(ValueError, message="'%' is an invalid character for this instance of a 'IndexSerializer'"):
        serializer.parse("000000%")

    with raises(TypeError, message="serialize() 'index' argument must be an 'int' like object not 'object'"):
        serializer.serialize(object())

    with raises(ValueError, message="serialize() 'index' argument must be between 0 and 78364164096"):
        serializer.serialize(-1)


def test_number_serialize():
    zero_serial = "          +0"
    tolerance = 10 ** -10
    serializer = NumberSerializer(length=12, capitals=True, tolerance=tolerance)

    for _ in range(1000):
        number = random_number(10)
        serial = serializer.serialize(number)
        parsed = serializer.parse(serial)

        if abs(number) <= tolerance:
            assert serial == zero_serial
            assert parsed == 0
        else:
            assert_number(number, parsed, -5)

    for _ in range(1000):
        number = random_number(150)
        serial = serializer.serialize(number)
        parsed = serializer.parse(serial)

        if abs(number) <= tolerance:
            assert serial == zero_serial
            assert parsed == 0
        else:
            assert_number(number, parsed, -4)


def test_number_serialize_exceptions():
    serializer = NumberSerializer(length=12, capitals=True, tolerance=10 ** -10)

    with raises(TypeError, message="'length' argument must be an 'int' like object not 'object'"):
        NumberSerializer(length=object())

    with raises(ValueError, message="'length' argument must be greater than 8"):
        NumberSerializer(length=8)

    with raises(TypeError, message="parse() argument must be a 'str', not 'object'"):
        serializer.parse(object())

    with raises(TypeError, message="serialize() 'number' argument must be an number like object not 'object'"):
        serializer.serialize(object())
