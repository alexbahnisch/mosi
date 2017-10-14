#!/usr/bin/env python
from ..format import GLPKSolutionReader as _GLPKSolutionReader, LPWriter as _LPWriter, MPSWriter as _MPSWriter
from .cli import FileTypes as _FileTypes, CliSolver as _CliSolver


class GlpkCliSolver(_CliSolver):
    def __init__(self, path, file_type="mps"):
        file_type = _FileTypes.parse(file_type)

        if file_type == _FileTypes.lp:
            super().__init__("--lp", path=path, model_writer_class=_LPWriter, solution_reader_class=_GLPKSolutionReader)
        else:
            super().__init__("--mps", path=path, model_writer_class=_MPSWriter, solution_reader_class=_GLPKSolutionReader)

    def solve(self, model, directory=None, name=None, delete=True, message_callback=print, **cli_args):
        self._pre_solve(directory, name, delete)

        cli_args = [
            self._model_writer.get_path(),
            *self._cli_args,
            *cli_args,
            "--output", self._solution_reader.get_path()
        ]

        self._solver(model, cli_args, message_callback)
