from ...common import ModelStatus as _ModelStatus
from .base import TxtSolutionReader as _TxtSolutionReader


class LPSolveSolutionReader(_TxtSolutionReader):
    __STATUS__ = {
        "Actual values of the variables:": _ModelStatus.OPTIMAL,
        "This problem is unbounded": _ModelStatus.UNBOUND,
        "This problem is infeasible": _ModelStatus.INFEASIBLE
    }

    def __init__(self, directory=None, name=None, delete=True):
        super().__init__(directory, name, ".sol.lps", delete)

    def _parse_line(self, model, line):
        cells = line.replace(self.__NEWLINE__, "").split(self.__DELIMITER__)
        cells = [cell for cell in cells if cell != ""]

        try:
            self._model.set_variable_value(self.__KEYPARSER__(cells[0]), self.__VALUEPARSER__(cells[1]))
        except (ValueError, IndexError):
            pass

        try:
            self._model.set_status(self._read_status(line.replace(self.__NEWLINE__, "")))
        except (KeyError, IndexError):
            pass
