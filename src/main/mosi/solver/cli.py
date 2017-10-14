#!/usr/bin/env python
from functools import wraps as _wraps
from subprocess import Popen as _Popen, PIPE as _PIPE

from pyplus.common import ispathlike as _ispathlike, iswindows as _iswindows
from pyplus.path import LazyPath as _LazyPath

from ..common import BaseEnum as _BaseEnum, BaseObject as _BaseObject
from ..format import ModelWriter as _ModelWriter, SolutionReader as _SolutionReader


def solverpath(method):
    @_wraps(method)
    def wrapped(self, path):
        if path is None or _ispathlike(path):
            method(self, path)
        else:
            raise TypeError("'path' argument must be and instance of str, NoneType or pathlib.Path, not '%s'" % type(path).__name__)

    return wrapped


# noinspection PyClassHasNoInit
class FileTypes(_BaseEnum):
    lp = "lp"
    mps = "mps"


class CliSolver(_BaseObject):
    __HELP__ = "-h"
    __EXE__ = "clisolver"

    def __init__(self, *args, path=None, model_writer_class=None, solution_reader_class=None):
        self._solver_path = None
        self._model_writer_class = _ModelWriter.issubclass(model_writer_class)
        self._model_writer = None
        self._solution_reader_class = _SolutionReader.issubclass(solution_reader_class)
        self._solution_reader = None
        self._cli_args = args

        self._set_solver_path(path)
        self._solver_path.resolve()

    @solverpath
    def _set_solver_path(self, path):
        if path is None:
            self._solver_path = _LazyPath(self.__EXE__ + ".exe" if _iswindows() else "")
        else:
            self._solver_path = _LazyPath(path)

    def _run(self, args, message_callback):
        args = [self.get_path(), *args]
        process = _Popen(args, stdout=_PIPE, universal_newlines=True)

        while process.poll() is None:
            stdout = process.stdout.readline()
            if stdout != "":
                stdout = stdout.replace("\n", "")
                if stdout != "":
                    message_callback(stdout)

        stdout = process.stdout.readline()
        while stdout != "":
            stdout = stdout.replace("\n", "")
            if stdout != "":
                message_callback(stdout)
            stdout = process.stdout.readline()

    def _pre_solve(self, directory, name, delete):
        self._model_writer = self._model_writer_class(directory=directory, name=name, delete=delete)
        self._solution_reader = self._solution_reader_class(directory=directory, name=name, delete=delete)

    def _solve(self, model, cli_args, message_callback):
        self._model_writer.write(model)
        self._run(cli_args, message_callback)
        self._solution_reader.read(model)
        self._model_writer.delete()
        self._solution_reader.delete()

    def get_help(self, message_callback=print):
        self._run(self.__HELP__, message_callback)

    def get_path(self):
        return str(self._solver_path)

    def solve(self, model, directory=None, name=None, delete=True, *cli_args):
        pass
