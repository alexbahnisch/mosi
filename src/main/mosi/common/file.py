#!/usr/bin/env python
from datetime import datetime
from os import remove
from pathlib import Path
from tempfile import mkdtemp

from .base import BaseModel, BaseObject


class ModelFile(BaseObject):

    def __init__(self, model, directory=None, name=None, extension=".txt", delete=True):
        self._model = BaseModel.isinstance(model)
        self._base_name = str(name) if name else model.get_name() + "_" + datetime.now().strftime("%Y%m%d%H%M%S")
        self._extension = str(extension)
        self._delete = bool(delete)

        self._base_directory = None
        self._path = None

        self._set_base_directory(directory)
        self._set_directory(directory)
        self._set_name()

    def __del__(self):
        if self._delete:
            self.delete()

    def _set_base_directory(self, directory):
        path = Path(str(directory)).resolve()

        for parent in path.parents:
            if parent.exists():
                self._base_directory = parent.resolve()
                break

    def _set_directory(self, directory):
        directory = str(directory)
        try:
            self._path = Path(directory).resolve()
            if not self._path.exists():
                self._path.mkdir()

        except (TypeError, FileExistsError):
            self._path = Path(mkdtemp()).resolve()
            self._path.mkdir()

    def _set_name(self):
        path = self._path.joinpath(str(self._base_name) + str(self._extension))
        index = 0

        while path.exists():
            index += 1
            path = self._path.joinpath(str(self._base_name) + ("(%s)" % index) + str(self._extension))

        self._path = path
        self._path.touch()

    def delete(self):
        if self._path.is_file():
            remove(str(self._path))

        for parent in self._path.parents:
            if parent > self._base_directory:
                try:
                    parent.rmdir()
                except OSError:
                    break

    def get_directory(self):
        return str(self._path.parent)

    @property
    def directory(self):
        return str(self._path.parent)

    def get_name(self):
        return self._path.name[0: -len(self._extension)]

    @property
    def name(self):
        return self._path.name[0: -len(self._extension)]

    def get_path(self):
        return str(self._path)

    @property
    def path(self):
        return str(self._path)

    def read(self):
        return self._path.open(mode="r")

    def write(self):
        return self._path.open(mode="w")
