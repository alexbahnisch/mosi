#!/usr/bin/env python
from pathlib import Path

from ..format import CBCSolutionReader as _CBCSolutionReader, LPWriter as _LPWriter, MPSWriter as _MPSWriter
from .cli import FileTypes as _FileTypes, CliSolver as _CliSolver, solverpath as _solverpath


# noinspection PyUnresolvedReferences
class CbcCliSolver(_CliSolver):
    __EXE__ = "cbc"

    def __init__(self, path=None, file_type="mps"):
        file_type = _FileTypes.parse(file_type)

        if file_type == _FileTypes.lp:
            super(CbcCliSolver, self).__init__(path=path, model_writer_class=_LPWriter, solution_reader_class=_CBCSolutionReader)
        elif file_type == _FileTypes.mps:
            super(CbcCliSolver, self).__init__(path=path, model_writer_class=_MPSWriter, solution_reader_class=_CBCSolutionReader)
        else:
            super(CbcCliSolver, self).__init__(path=path, model_writer_class=_MPSWriter, solution_reader_class=_CBCSolutionReader)

    @_solverpath
    def _set_solver_path(self, path):
        if path is None:
            try:
                import mosi_cbc
                if mosi_cbc.__version__ >= "0.0.1":
                    self._solver_path = Path(mosi_cbc.get_cbc_path())
            except ImportError:
                pass

        if self._solver_path is None:
            super()._set_solver_path(path)

    def solve(self, model, directory=None, name=None, delete=True, message_callback=print, *cli_args):
        self._pre_solve(directory, name, delete)

        cli_args = [
            self._model_writer.get_path(),
            *self._cli_args,
            *cli_args,
            "solve",
            "solu", self._solution_reader.get_path(),
        ]

        self._solve(model, cli_args, message_callback)
