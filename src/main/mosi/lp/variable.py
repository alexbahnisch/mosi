#!/usr/bin/env python
from decimal import Decimal
from math import inf

from .. import common as _
from .constraint import LinearConstraint
from .sum import LinearSum


# noinspection PyShadowingBuiltins
class DecisionVariable(_.BaseVariable):
    def __init__(self, model, min=0, max=inf, name=None, type=_.VariableType.FLOAT):
        self._model = _.BaseModel.isinstance(model)
        self._name = model.parse_variable_name(name)
        self._min = float(min)
        self._max = float(max)
        self._type = _.VariableType.parse(type)

        self._constraints = set()

        self._uid = None
        self._objective = None
        self._lower_bound_constraint = None
        self._upper_bound_constraint = None
        self._value = _.NoValue

    def __hash__(self):
        return id(self)

    def __pos__(self):
        return LinearSum(self._model, {self: 1})

    def __neg__(self):
        return LinearSum(self._model, {self: -1})

    def __add__(self, other):
        if isinstance(other, (Decimal, float, int)):
            return LinearSum(self._model, {self: 1}, other)
        elif isinstance(other, _.BaseVariable):
            return LinearSum(self._model, {self: 1, other: 1})
        elif isinstance(other, _.BaseSum):
            pass
        else:
            _.raise_operand_error(self, other, "+")

    def __iadd__(self, other):
        if isinstance(other, (Decimal, float, int)):
            return LinearSum(self._model, {self: 1}, other)
        elif isinstance(other, _.BaseVariable):
            return LinearSum(self._model, {self: 1, other: 1})
        elif isinstance(other, _.BaseSum):
            pass
        else:
            _.raise_operand_error(self, other, "+=")

    def __radd__(self, other):
        if isinstance(other, (Decimal, float, int)):
            return LinearSum(self._model, {self: 1}, other)
        elif isinstance(other, _.BaseVariable):
            return LinearSum(self._model, {self: 1, other: 1})
        elif isinstance(other, _.BaseSum):
            pass
        else:
            _.raise_operand_error(other, self, "+")

    def __sub__(self, other):
        if isinstance(other, (Decimal, float, int)):
            return LinearSum(self._model, {self: 1}, -other)
        elif isinstance(other, _.BaseVariable):
            return LinearSum(self._model, {self: 1, other: -1})
        elif isinstance(other, _.BaseSum):
            pass
        else:
            _.raise_operand_error(other, self, "-")

    def __isub__(self, other):
        if isinstance(other, (Decimal, float, int)):
            return LinearSum(self._model, {self: 1}, -other)
        elif isinstance(other, _.BaseVariable):
            return LinearSum(self._model, {self: 1, other: -1})
        elif isinstance(other, _.BaseSum):
            pass
        else:
            _.raise_operand_error(other, self, "-=")

    def __rsub__(self, other):
        if isinstance(other, (Decimal, float, int)):
            return LinearSum(self._model, {self: -1}, other)
        elif isinstance(other, _.BaseVariable):
            return LinearSum(self._model, {self: -1, other: 1})
        elif isinstance(other, _.BaseSum):
            pass
        else:
            _.raise_operand_error(other, self, "-")

    def __mul__(self, other):
        if isinstance(other, (Decimal, float, int)):
            return LinearSum(self._model, {self: other})
        else:
            # TODO - add non-linear exception
            _.raise_operand_error(other, self, "*")

    def __imul__(self, other):
        if isinstance(other, (Decimal, float, int)):
            return LinearSum(self._model, {self: other})
        else:
            # TODO - add non-linear exception
            _.raise_operand_error(other, self, "*=")

    def __rmul__(self, other):
        if isinstance(other, (Decimal, float, int)):
            return LinearSum(self._model, {self: other})
        else:
            # TODO - add non-linear exception
            _.raise_operand_error(other, self, "*")

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError("division by zero")
        if isinstance(other, (Decimal, float, int)):
            return LinearSum(self._model, {self: Decimal(1) / other})
        else:
            # TODO - add non-linear exception
            _.raise_operand_error(self, other, "/")

    def __idiv__(self, other):
        if other == 0:
            raise ZeroDivisionError("division by zero")
        if isinstance(other, (Decimal, float, int)):
            return LinearSum(self._model, {self: Decimal(1) / other})
        else:
            # TODO - add non-linear exception
            _.raise_operand_error(self, other, "/=")

    def __rdiv__(self, other):
        # TODO - add non-linear exception
        _.raise_operand_error(other, self, "/")

    def __eq__(self, other):
        if isinstance(other, (Decimal, float, int)):
            return LinearConstraint(self._model, {self: 1}, other, _.ConstraintType.EQ)
        elif isinstance(other, _.BaseVariable):
            return LinearConstraint(self._model, {self: 1, other: -1}, 0, _.ConstraintType.EQ)
        elif isinstance(other, _.BaseSum):
            pass
        else:
            _.raise_operand_error(self, other, "==")

    def __ge__(self, other):
        if isinstance(other, (Decimal, float, int)):
            return LinearConstraint(self._model, {self: 1}, other, _.ConstraintType.GE)
        elif isinstance(other, _.BaseVariable):
            return LinearConstraint(self._model, {self: 1, other: -1}, 0, _.ConstraintType.GE)
        elif isinstance(other, _.BaseSum):
            pass
        else:
            _.raise_operand_error(self, other, ">=")

    def __le__(self, other):
        if isinstance(other, (Decimal, float, int)):
            return LinearConstraint(self._model, {self: 1}, other, _.ConstraintType.LE)
        elif isinstance(other, _.BaseVariable):
            return LinearConstraint(self._model, {self: 1, other: -1}, 0, _.ConstraintType.LE)
        elif isinstance(other, _.BaseSum):
            pass
        else:
            _.raise_operand_error(self, other, "<=")

    @classmethod
    def dict(cls, model, *keyss, min=0, max=inf, name=None, type=_.VariableType.FLOAT):
        _.make_dict(cls, *keyss, model=model, min=min, max=max, name=name, type=type)

    @classmethod
    def list(cls, model, *dimensions, min=0, max=inf, name=None, type=_.VariableType.FLOAT):
        _.make_dict(cls, *dimensions, model=model, min=min, max=max, name=name, type=type)

    @classmethod
    def tuple_dict(cls, model, *keyss, min=0, max=inf, name=None, type=_.VariableType.FLOAT):
        _.make_dict(cls, *keyss, model=model, min=min, max=max, name=name, type=type)

    def add_constraint(self, constraint):
        self._constraints.add(constraint)

    def clear(self):
        self._value = _.NoValue

        if self._lower_bound_constraint is not None:
            self._model.remove_constraint(self._lower_bound_constraint)
            self._lower_bound_constraint = None

        if self._upper_bound_constraint is not None:
            self._model.remove_constraint(self._upper_bound_constraint)
            self._upper_bound_constraint = None

    def is_in_constraint(self):
        return len(self._constraints) > 0

    def is_in_objective(self):
        return self._objective is not None

    def get_constraints(self):
        return self._constraints

    @property
    def constraints(self):
        return self._constraints

    def get_uid(self):
        return self._uid

    @property
    def uid(self):
        return self._uid

    def get_lower_bound(self):
        return self._min

    @property
    def lower_bound(self):
        return self._min

    def get_model(self):
        return self._model

    @property
    def model(self):
        return self._model

    def get_name(self):
        return self._name

    @property
    def name(self):
        return self._name

    def get_upper_bound(self):
        return self._max

    @property
    def upper_bound(self):
        return self._max

    def get_value(self):
        return self._value

    @property
    def value(self):
        return self._value

    def has_uid(self):
        return self._uid is not None

    def has_value(self):
        return self._value is not _.NoValue

    def remove_constraint(self, constraint):
        if constraint in self._constraints:
            self._constraints.remove(constraint)

    def remove_objective(self):
        self._objective = None

    def set_uid(self, uid):
        self._uid = uid

    def set_objective(self, objective):
        self._objective = objective

    def set_lower_bound_constraint(self, lower_bound=None):
        if lower_bound is None:
            self._lower_bound_constraint = self >= self._min
        else:
            self._lower_bound_constraint = self >= float(lower_bound)

    def set_upper_bound_constraint(self, upper_bound=None):
        if upper_bound is None:
            self._upper_bound_constraint = self <= self._max
        else:
            self._upper_bound_constraint = self <= float(upper_bound)

    def set_value(self, value):
        self._value = self._type.parse_solution(value)


# noinspection PyShadowingBuiltins
class FloatVariable(DecisionVariable):
    def __init__(self, model, min=0, max=inf, name=None):
        super().__init__(model, min, max, name, type=_.VariableType.FLOAT)

    @classmethod
    def dict(cls, model, *keyss, min=0, max=inf, name=None):
        super().dict(model, *keyss, min=min, max=max, name=name, type=_.VariableType.FLOAT)

    @classmethod
    def list(cls, model, *dimensions, min=0, max=inf, name=None):
        super().list(model, *dimensions, min=min, max=max, name=name, type=_.VariableType.FLOAT)

    @classmethod
    def tuple_dict(cls, model, *keyss, min=0, max=inf, name=None):
        super().tuple_dict(model, *keyss, min=min, max=max, name=name, type=_.VariableType.FLOAT)
