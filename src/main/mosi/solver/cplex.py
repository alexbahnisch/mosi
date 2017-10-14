#!/usr/bin/env python
from os import remove as _remove

from ..format import CplexSolutionReader as _CplexSolutionReader, LPWriter as _LPWriter, MPSWriter as _MPSWriter
from .cli import FileTypes as _FileTypes, CliSolver as _CliSolver


class CplexCliSolver(_CliSolver):
    __HELP__ = "help"
    __EXE__ = "cplex"

    def __init__(self, path, file_type="mps"):
        file_type = _FileTypes.parse(file_type)

        if file_type == _FileTypes.lp:
            super().__init__(path=path, model_writer_class=_LPWriter, solution_reader_class=_CplexSolutionReader)
        elif file_type == _FileTypes.mps:
            super().__init__(path=path, model_writer_class=_MPSWriter, solution_reader_class=_CplexSolutionReader)
        else:
            super().__init__(path=path, model_writer_class=_MPSWriter, solution_reader_class=_CplexSolutionReader)

    def _run(self, args, message_callback):
        args = ["-c", *args, "quit"]
        super()._run(args, message_callback)

    def solve(self, model, directory=None, name=None, delete=True, message_callback=print, *cli_args):
        self._pre_solve(directory, name, delete)

        cli_args = [
            "read", self._model_writer.get_path(),
            *self._cli_args,
            *cli_args,
            "optimize",
            "write", self._solution_reader.get_path(), "y",
        ]

        self._solve(model, cli_args, message_callback)
        _remove("cplex.log")
