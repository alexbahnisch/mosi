from pyplus.path import LazyPath as _LazyPath

from .base import BaseObject as _BaseObject


class ModelFile(_BaseObject):

    def __init__(self, directory=None, name=None, extension=".txt", delete=True):
        self._path = _LazyPath.new_file(dir=directory, prefix=name, suffix=extension)
        self._delete = delete

    @property
    def path(self):
        return self._path

    def delete(self, force=False):
        if self._delete or force:
            self._path.delete()

    def get_path(self):
        return str(self._path)
