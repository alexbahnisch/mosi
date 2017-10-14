#!/usr/bin/env python
from io import StringIO

from .base import ModelWriter as _ModelWriter


class LPWriter(_ModelWriter):

    def __init__(self, directory=None, name=None, delete=True):
        super().__init__(directory, name, ".lp", delete)

    def write(self, model):
        variable_file = StringIO()

        with self._path.write() as file:
            self._write_prefix(file, model)
            self._write_variables(variable_file, model)
            self._write_objective(file, model)
            self._write_constraints(file, model)
            file.write(variable_file.getvalue())
            self._write_suffix(file)

        variable_file.close()

    @staticmethod
    def _get_bounds(variable):
        bounds = ""
        variable_type = None

        if variable.has_value():
            bounds = "%s = %s\n" % (variable.get_uid(), variable.get_value())

        elif variable.get_lower_bound() == -float("inf") and variable.get_upper_bound() == float("inf"):
            bounds = "%s free\n" % variable.get_uid()

        elif variable.get_lower_bound() != 0 and variable.get_upper_bound() < float("inf"):
            bounds = "%s <= %s <= %s\n" % (variable.get_lower_bound(), variable.get_uid(), variable.get_upper_bound())

        elif variable.get_lower_bound() != 0:
            bounds = "%s <= %s\n" % (variable.get_lower_bound(), variable.get_uid())

        elif variable.get_upper_bound() < float("inf"):
            bounds = "%s <= %s\n" % (variable.get_uid(), variable.get_upper_bound())

        return bounds, variable_type

    @staticmethod
    def _parse_value(value):
        if value == 0:
            return None
        else:
            string = "+" if value > 0 else "-"
            string += "%s" % abs(value) if abs(value) != 1 else ""

            return string

    def _write_constraints(self, file, model):
        constraints = model.get_constraints()
        file.write("SUBJECT TO\n")

        for (index, constraint) in enumerate(constraints):
            key = "c%s" % index
            constraint.set_uid(key)
            file.write(key + ":")

            for variable in constraint:
                value = self._parse_value(constraint[variable])
                if value is not None:
                    file.write(" %s %s" % (value, variable.get_uid()))

            file.write(" %s %s\n" % (constraint.get_type().to_lp(), constraint.get_constant()))

    def _write_objective(self, file, model):
        objective = model.get_objective()
        file.write(objective.get_type().to_lp() + "\n")
        file.write("obj:")

        for variable in objective:
            value = self._parse_value(objective[variable])
            if value is not None:
                file.write(" %s %s" % (value, variable.get_uid()))

        file.write("\n")

    @staticmethod
    def _write_prefix(file, model):
        file.write("\%s\n" % model.get_name())

    @staticmethod
    def _write_suffix(file):
        file.write("END")

    def _write_variables(self, file, model):
        file.write("BOUNDS\n")
        variables = model.get_variables()

        for (index, variable) in enumerate(variables):
            key = "x%s" % index
            model.set_variable_key(variable, key)
            bounds, variable_type = self._get_bounds(variable)
            file.write(bounds)
