#!/usr/bin/env python
from functools import wraps
from pathlib import Path
from subprocess import Popen, PIPE

from ..common import BaseEnum, BaseObject


def solverpath(method):
    @wraps(method)
    def wrapped(self, path):
        if path is None or isinstance(path, (str, Path)):
            method(self, path)
        else:
            raise TypeError(
                "'path' argument must be and instance of str, NoneType or pathlib.Path, not '%s'" % type(path).__name__
            )

    return wrapped


class FileTypes(BaseEnum):
    lp = "lp"
    mps = "mps"


class CliSolver(BaseObject):
    __HELP__ = "-h"
    __EXE__ = None

    def __init__(self, *args, path=None, model_writer=None, solution_reader=None):
        self._solver_path = None
        self._model_writer = model_writer
        self._solution_reader = solution_reader
        self._cli_args = args

        self._set_solver_path(path)
        self._solver_path.resolve()

    @solverpath
    def _set_solver_path(self, path):
        if path is None:
            self._solver_path = Path(self.__EXE__)
        else:
            self._solver_path = Path(path)

    @staticmethod
    def _run(args, message_callback):
        process = Popen(args, stdout=PIPE, universal_newlines=True)

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

    def get_help(self, message_callback=print):
        self._run(self.__HELP__, message_callback)

    def get_path(self):
        return str(self._solver_path)

    def solve(self, model, *args, directory=None, name=None, delete=True):
        pass
