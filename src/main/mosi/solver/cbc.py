#!/usr/bin/env python
from pathlib import Path

from ..io import CbcSolutionFile, CbcSolutionReader, LpWriter, MpsWriter
from .base import FileTypes, CliSolver, solverpath


# noinspection PyUnresolvedReferences
class CbcCliSolver(CliSolver):
    __EXE__ = "cbc.exe"

    def __init__(self, path=None, file_type="mps"):
        file_type = FileTypes.parse(file_type)

        if file_type == FileTypes.lp:
            super(CbcCliSolver, self).__init__(path=path, model_writer=LpWriter(), solution_reader=CbcSolutionReader())
        elif file_type == FileTypes.mps:
            super(CbcCliSolver, self).__init__(path=path, model_writer=MpsWriter(), solution_reader=CbcSolutionReader())
        else:
            super(CbcCliSolver, self).__init__(path=path, model_writer=MpsWriter(), solution_reader=CbcSolutionReader())

    @solverpath
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

    def solve(self, model, directory=None, name=None, delete=True, message_callback=print, **kwargs):
        self._model_writer.set(directory, name, bool(delete))
        self._solution_reader.set(model)

        model_file = self._model_writer(model)
        solution_file = CbcSolutionFile(model, model_file.get_directory(), model_file.get_name(), delete)

        args = [
            self.get_path(), model_file.get_path(),
            *self._cli_args,
            "solve",
            "solu", solution_file.get_path(),
        ]

        self._run(args, message_callback)
        self._solution_reader(solution_file)
