#!/usr/bin/env python
from mosi.common import BaseEnum, BaseIntEnum, ConstraintType, ModelStatus, ObjectiveType, VariableType
from pytest import raises


class TestEnum(BaseEnum):
    FALSE = "FALSE"
    TRUE = "TRUE"


class TestIntEnum(BaseIntEnum):
    FALSE = 0
    TRUE = 1


def test_base_enum_exception():
    with raises(ValueError, message="'ERROR' is not a valid 'TestEnum'"):
        TestEnum.parse("ERROR")

    with raises(ValueError, message="'2' is not a valid 'TestEnum'"):
        TestEnum.parse(2)


def test_base_enum_parse():
    assert TestEnum.FALSE == TestEnum.parse(TestEnum.FALSE)
    assert TestEnum.FALSE == TestEnum.parse("FALSE")
    assert TestEnum.FALSE == TestEnum.parse("false")

    assert TestEnum.TRUE == TestEnum.parse(TestEnum.TRUE)
    assert TestEnum.TRUE == TestEnum.parse("TRUE")
    assert TestEnum.TRUE == TestEnum.parse("true")


def test_base_int_enum_exception():
    with raises(ValueError, message="'ERROR' is not a valid 'TestEnum'"):
        TestIntEnum.parse("ERROR")

    with raises(ValueError, message="'2' is not a valid 'TestEnum'"):
        TestIntEnum.parse(2)


def test_base_int_enum_parse():
    assert TestIntEnum.FALSE == TestIntEnum.parse(TestIntEnum.FALSE)
    assert TestIntEnum.FALSE == TestIntEnum.parse(0)
    assert TestIntEnum.FALSE == TestIntEnum.parse(0.0)
    assert TestIntEnum.FALSE == TestIntEnum.parse("0")
    assert TestIntEnum.FALSE == TestIntEnum.parse("FALSE")
    assert TestIntEnum.FALSE == TestIntEnum.parse("false")

    assert TestIntEnum.TRUE == TestIntEnum.parse(TestIntEnum.TRUE)
    assert TestIntEnum.TRUE == TestIntEnum.parse(1)
    assert TestIntEnum.TRUE == TestIntEnum.parse(1.0)
    assert TestIntEnum.TRUE == TestIntEnum.parse("1")
    assert TestIntEnum.TRUE == TestIntEnum.parse("TRUE")
    assert TestIntEnum.TRUE == TestIntEnum.parse("true")


def test_model_status_exceptions():
    with raises(ValueError, message="'SOLVED' is not a valid 'ModelStatus'"):
        ModelStatus("SOLVED")

    with raises(ValueError, message="'solved' is not a valid 'ModelStatus'"):
        ModelStatus.parse("solved")

    with raises(ValueError, message="'10' is not a valid 'ModelStatus'"):
        ModelStatus.parse(10)

    with raises(ValueError, message="'SOLVED' is not a valid 'ModelStatus'"):
        ModelStatus.parse("SOLVED")

    with raises(ValueError, message="'solved' is not a valid 'ModelStatus'"):
        ModelStatus("solved")

    with raises(ValueError, message="'solved' is not a valid 'ModelStatus'"):
        ModelStatus(10)


def test_constraint_type_inverse():
    eq = ConstraintType.EQ
    ge = ConstraintType.GE
    le = ConstraintType.LE

    assert ConstraintType.EQ == ~eq
    assert ConstraintType.GE == ~le
    assert ConstraintType.LE == ~ge

    assert ConstraintType.GE == ge
    assert ConstraintType.LE == le


def test_constraint_type_to_lp():
    assert "=" == ConstraintType.EQ.to_lp()
    assert ">=" == ConstraintType.GE.to_lp()
    assert "<=" == ConstraintType.LE.to_lp()


def test_constraint_type_to_mp():
    assert "E" == ConstraintType.EQ.to_mps()
    assert "G" == ConstraintType.GE.to_mps()
    assert "L" == ConstraintType.LE.to_mps()


def test_model_status_is_solved():
    assert ModelStatus.OPTIMAL.is_solved()
    assert not ModelStatus.UNSOLVED.is_solved()
    assert not ModelStatus.UNBOUND.is_solved()
    assert not ModelStatus.INFEASIBLE.is_solved()
    assert not ModelStatus.UNDEFINED.is_solved()


def test_objective_type_inverse():
    max_ = ObjectiveType.MAX
    min_ = ObjectiveType.MIN

    assert ObjectiveType.MAX == ~min_
    assert ObjectiveType.MIN == ~max_

    assert ObjectiveType.MAX == max_
    assert ObjectiveType.MIN == min_


def test_objective_type_to_lp():
    assert "MAXIMIZE" == ObjectiveType.MAX.to_lp()
    assert "MINIMIZE" == ObjectiveType.MIN.to_lp()


def test_objective_type_to_mp():
    assert "MAX" == ObjectiveType.MAX.to_mps()
    assert "MIN" == ObjectiveType.MIN.to_mps()


def test_variable_type_float_parser():
    strings = [" +1", "-10 ", "0.3"]
    numbers = [1, -10, 0.3]

    var_types = [VariableType.FLOAT, VariableType.SEMI_CONTINUOUS]

    for var_type in var_types:
        parser = var_type.parse_solution
        for string, number in zip(strings, numbers):
            assert number == parser(string)


def test_variable_type_int_parser():
    strings = [" +1", "-10 ", "0.1", "0.9"]
    numbers = [1, -10, 0, 1]

    var_types = [VariableType.INTEGER, VariableType.SEMI_INTEGER]

    for var_type in var_types:
        parser = var_type.parse_solution
        for string, number in zip(strings, numbers):
            assert number == parser(string)
