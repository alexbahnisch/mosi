from xml.etree.ElementTree import parse as _parse, ParseError as _ParseError

from ...common import BaseModel as _BaseModel, ModelStatus as _ModelStatus
from .base import SolutionReader


class CplexSolutionReader(SolutionReader):
    __STATUS__ = {
        "optimal": _ModelStatus.OPTIMAL
    }

    def __init__(self, directory=None, name=None, delete=True):
        super().__init__(directory, name, ".sol", delete)

    def write(self, model):
        model = _BaseModel.isinstance(model)

        try:
            root_element = _parse(str(self._path)).getroot()
            for element in root_element:
                if element.tag == "header":
                    model.set_status(self.__KEYPARSER__(element.attrib["solutionStatusString"]))

                if element.tag == "variables":
                    for child_element in element:
                        self._parse_element(model, child_element)
        except _ParseError:
            model.set_status(_ModelStatus.UNDEFINED)

    def _parse_element(self, model, element):
        attributes = element.attrib
        model.set_variable_value(
            self.__KEYPARSER__(attributes["name"]), self.__VALUEPARSER__(attributes["value"])
        )
