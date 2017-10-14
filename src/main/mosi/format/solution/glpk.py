from ...common import ModelStatus as _ModelStatus
from .base import TxtSolutionReader as _TxtSolutionReader


class GLPKSolutionReader(_TxtSolutionReader):
    __STATUS__ = {
        "OPTIMAL": _ModelStatus.OPTIMAL,
        "UNDEFINED": _ModelStatus.UNDEFINED
    }

    def __init__(self, directory=None, name=None, delete=True):
        super().__init__(directory, name, ".sol.glpk", delete)

    def _parse_line(self, model, line):
        cells = line.replace(self.__NEWLINE__, "").split(self.__DELIMITER__)
        cells = [cell for cell in cells if cell != ""]

        try:
            model.set_variable_value(self.__KEYPARSER__(cells[1]), self.__VALUEPARSER__(cells[3]))
        except (ValueError, IndexError):
            pass

        try:
            model.set_status(self._read_status(self.__KEYPARSER__(cells[1])))
        except (KeyError, IndexError):
            pass
