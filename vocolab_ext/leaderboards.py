import abc
from pathlib import Path
from typing import Dict

from .base import PluginRegistry


class LeaderboardManager(abc.ABC):
    """A class allowing to manage leaderboard objects"""

    @classmethod
    @abc.abstractmethod
    def load_from_obj(cls, name: str, obj: Dict):
        """Load self from an object"""
        pass

    @abc.abstractmethod
    def export_as_csv(self, file: Path):
        pass


class LeaderboardRegistry(PluginRegistry):
    """Registry for leaderboard managers"""

    def __init__(self):
        super().__init__('leaderboards')

    def load(self, name) -> LeaderboardManager:
        entry = self._entry(name)
        return self._load_obj(entry)


def list_items():
    """ List registered leaderboard managers """
    reg = LeaderboardRegistry()
    for item in reg.names:
        print(reg.load(item))
