#!/usr/bin/env python
from copy import copy
from io import StringIO

from ... import common as _c
from .base import ModelWriter as _ModelWriter


# noinspection PyClassHasNoInit
class MpsBoundTypes(_c.BaseEnum):
    LO = "LO"
    UP = "UP"
    FX = "FX"
    FR = "FR"
    MI = "MI"


class MPSWriter(_ModelWriter):

    def __init__(self, directory=None, name=None, delete=True):
        super().__init__(directory, name, ".mps", delete)
        self._index_serializer = _c.IndexSerializer(length=7, capitals=True)
        self._number_serializer = _c.NumberSerializer(length=12, capitals=True, tolerance=10 ** -10)

    def write(self, model):
        variables_file = StringIO()

        with self._path.write() as file:
            self._write_prefix(file, model)
            self._write_variables(variables_file, model)
            self._write_rows(file, model)
            self._write_columns(file, model)
            self._write_rhs(file, model)
            file.write(variables_file.getvalue())
            self._write_suffix(file)

        variables_file.close()

    @staticmethod
    def _get_bounds(variable):
        bound_format = " %s bound     %s  %s\n"
        bounds = []

        if variable.get_lower_bound() == 0 and variable.get_upper_bound() == float("inf"):
            pass

        elif variable.has_value() or (variable.get_lower_bound() == variable.get_upper_bound()):
            bounds.append(bound_format % (MpsBoundTypes.FX, variable.get_uid(), variable.get_value()))

        elif variable.get_lower_bound() >= 0:

            if variable.get_lower_bound() > 0:
                bounds.append(bound_format % (MpsBoundTypes.LO, variable.get_uid(), variable.get_lower_bound()))

            if variable.get_upper_bound() < float("inf"):
                bounds.append(bound_format % (MpsBoundTypes.UP, variable.get_uid(), variable.get_upper_bound()))

        elif variable.get_upper_bound() <= 0:
            bounds.append(bound_format % (MpsBoundTypes.MI, variable.get_uid(), ""))

            if variable.get_lower_bound() > -float("inf"):
                variable.set_lower_bound_constraint()

            if variable.get_upper_bound() < 0:
                variable.set_upper_bound_constraint()

        else:
            bounds.append(bound_format % (MpsBoundTypes.FR, variable.get_uid(), ""))

            if variable.get_lower_bound() > -float("inf"):
                variable.set_lower_bound_constraint()

            if variable.get_upper_bound() < float("inf"):
                variable.set_upper_bound_constraint()

        return bounds

    @staticmethod
    def _write_prefix(file, model):
        file.write("NAME          %s\n" % model.get_name())

    @staticmethod
    def _write_suffix(file):
        file.write("ENDATA\n")

    def _write_rows(self, file, model):
        file.write("ROWS\n N  obj\n")

        for (index, constraint) in enumerate(model.get_constraints()):
            constraint.set_uid("c" + self._index_serializer.serialize(index))
            file.write(" %s  %s\n" % (constraint.get_type().to_mps(), constraint.get_uid()))

    def _write_columns(self, file, model):
        file.write("COLUMNS\n")
        objective = copy(model.get_objective())

        if objective.get_type() == _c.ObjectiveType.MAX:
            _ = ~objective
            inverse = True
        else:
            inverse = False

        for (column_index, variable) in enumerate(model.get_variables()):
            key = "x" + self._index_serializer.serialize(column_index)
            model.set_variable_key(variable, key)

            if variable.is_in_objective():
                new_line = False
                file.write("    %s  obj       %s" % (key, self._number_serializer.serialize(objective[variable])))
            else:
                new_line = True

            for constraint in variable.get_constraints():
                if new_line:
                    file.write(
                        "    %s  %s  %s" % (key, constraint.get_uid(), self._number_serializer.serialize(constraint[variable]))
                    )
                    new_line = False

                else:
                    file.write("   %s  %s\n" % (constraint.get_uid(), self._number_serializer.serialize(constraint[variable])))
                    new_line = True

            if not new_line:
                file.write("\n")

        if inverse:
            _ = ~objective

    def _write_rhs(self, file, model):
        file.write("RHS\n")
        new_line = True

        for (index, constraint) in enumerate(model.get_constraints()):
            if new_line:
                file.write(
                    "    rhs       %s  %s" % (constraint.get_uid(), self._number_serializer.serialize(constraint.get_constant()))
                )
                new_line = False
            else:
                file.write("   %s  %s\n" % (constraint.get_uid(), self._number_serializer.serialize(constraint.get_constant())))
                new_line = True

        if not new_line:
            file.write("\n")

    def _write_variables(self, file, model):
        file.write("BOUNDS\n")

        for (index, variable) in enumerate(model.get_variables()):
            index = "x" + self._index_serializer.serialize(index)
            variable.set_uid(index)
            bounds = self._get_bounds(variable)

            for bound in bounds:
                file.write(bound)
