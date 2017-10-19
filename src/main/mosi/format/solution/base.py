from ...common import BaseModel as _BaseModel, ModelFile as _ModelFile


# noinspection PyClassHasNoInit
class SolutionReader(_ModelFile):
    __KEYPARSER__ = str
    __VALUEPARSER__ = float
    __STATUS__ = {}

    def read(self, model):
        pass

    def _read_status(self, status):
        return self.__STATUS__[str(status)]


# noinspection PyClassHasNoInit
class TxtSolutionReader(SolutionReader):
    __DELIMITER__ = " "
    __NEWLINE__ = "\n"

    def read(self, model):
        model = _BaseModel.isinstance(model)

        with self._path.read() as file:
            lines = file.readlines()

            for line in lines:
                self._parse_line(model, line)

    def _parse_line(self, model, line):
        pass
