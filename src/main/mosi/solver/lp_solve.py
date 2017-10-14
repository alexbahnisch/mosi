#!/usr/bin/env python
from subprocess import Popen

from ..format import LPSolveSolutionReader as _LPSolveSolutionReader, LPSWriter as _LPSWriter, MPSWriter as _MPSWriter
from .cli import FileTypes as _FileTypes, CliSolver as _CliSolver


class LpSolveCliSolver(_CliSolver):

    def __init__(self, path, file_type="mps"):
        file_type = _FileTypes.parse(file_type)

        if file_type == _FileTypes.lp:
            super().__init__(path=path, model_writer_class=_LPSWriter, solution_reader_class=_LPSolveSolutionReader)
        elif file_type == _FileTypes.mps:
            super().__init__("-mps", path=path, model_writer_class=_MPSWriter, solution_reader_class=_LPSolveSolutionReader)
        else:
            super().__init__("-mps", path=path, model_writer_class=_MPSWriter, solution_reader_class=_LPSolveSolutionReader)

    def solve(self, model, directory=None, name=None, delete=True, message_callback=print, **cli_args):
        self._pre_solve(directory, name, message_callback)

        cli_args = [
            self._model_writer.get_path(),
            *self._cli_args,
            *cli_args
        ]

        with self._solution_reader.path.write() as output_file:
            Popen(cli_args, executable=self.get_path(), stdout=output_file).wait()

        self._solution_reader_class.read(model)
