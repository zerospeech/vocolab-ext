import abc
import importlib
import sys

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points


class PluginRegistry(abc.ABC):
    """Plugin Registry"""

    def __init__(self, namespace: str):
        # discover entrypoints
        self._entry_p = entry_points(group=f"vocolab_ext.{namespace}")

    @property
    def names(self):
        return self._entry_p.names

    def _entry(self, name: str):
        try:
            return self._entry_p[name]
        except KeyError:
            return None

    @staticmethod
    def _load_obj(entry):
        path, obj_name = tuple(entry.value.split(':'))
        lib = importlib.import_module(path)
        return getattr(lib, obj_name, None)

    @abc.abstractmethod
    def load(self, name):
        pass
