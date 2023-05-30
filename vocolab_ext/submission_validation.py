import abc
from pathlib import Path
from typing import Optional

from .base import PluginRegistry


class SubmissionValidator(abc.ABC):
    """A class allowing to manage leaderboard objects"""

    @classmethod
    @abc.abstractmethod
    def load_from_path(cls, location: Path):
        """Load self from an object"""
        pass

    @abc.abstractmethod
    def validate(self):
        pass


class SubmissionValidateRegistry(PluginRegistry):

    def __init__(self):
        super().__init__('submission_validation')

    def load(self, name) -> Optional[SubmissionValidator]:
        entry = self._entry(name)
        return self._load_obj(entry)


def list_items():
    """ List registered submission validators """
    reg = SubmissionValidateRegistry()
    for item in reg.names:
        print(reg.load(item))
