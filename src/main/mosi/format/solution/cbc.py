from ...common import ModelStatus as _ModelStatus
from .base import TxtSolutionReader as _TxtSolutionReader


class CBCSolutionReader(_TxtSolutionReader):
    __STATUS__ = {
        "Optimal": _ModelStatus.OPTIMAL,
        "Unbounded": _ModelStatus.UNBOUND,
        "Infeasible": _ModelStatus.INFEASIBLE
    }

    def __init__(self, directory=None, name=None, delete=True):
        super().__init__(directory, name, ".sol.cbc", delete)

    def _parse_line(self, model, line):
        cells = line.replace(self.__NEWLINE__, "").split(self.__DELIMITER__)
        cells = [cell for cell in cells if cell != ""]

        try:
            model.set_variable_value(self.__KEYPARSER__(cells[1]), self.__VALUEPARSER__(cells[2]))
        except (ValueError, IndexError):
            pass

        try:
            model.set_status(self._read_status(cells[0]))
        except KeyError:
            pass
