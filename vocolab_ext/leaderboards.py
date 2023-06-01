import abc
import json
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any, List, Union

if sys.version_info >= (3, 11):
    import tomllib  # noqa: does not exist in python_version < 3.11
else:
    try:
        import toml as tomllib
    except ImportError:
        tomllib = None

try:
    import yaml
except ImportError:
    yaml = None

from .base import PluginRegistry


def obj_load(location: Path) -> Union[Dict, List]:
    """ Load an object file """
    if location.suffix in ('.json',):
        with location.open() as fp:
            return json.load(fp)
    elif location.suffix in ('.yaml', '.yml'):
        if yaml is None:
            raise ImportError('Required module PyYAML to manage yaml files')

        with location.open() as fp:
            return yaml.load(fp, Loader=yaml.FullLoader)  # noqa: code not reached if module is none
    elif location.suffix in ('toml',):
        if yaml is None:
            raise ImportError('Required module toml to manage yaml files (or python >=3.11)')

        with location.open() as fp:
            return tomllib.load(fp)  # noqa: code not reached if module is none

    elif location.suffix in ('.txt', '.list'):
        with location.open() as fp:
            return fp.readlines()
    else:
        raise ValueError(f'File given {location} of unknown type !!')


@dataclass
class LeaderboardEntryBase:
    submission_id: str
    model_id: str
    description: str
    authors: str
    author_label: str
    submission_date: Optional[datetime]
    submitted_by: Optional[str]


class LeaderboardManager(abc.ABC):
    """A class allowing to manage leaderboard objects"""

    @classmethod
    def load_from_file(cls, name: str, location: Path):
        data = obj_load(location)
        return cls.load_leaderboard_from_obj(name, data)

    @classmethod
    @abc.abstractmethod
    def load_leaderboard_from_obj(cls, name: str, obj: Dict):
        """Load self from an object"""
        pass

    @classmethod
    def load_entry_from_file(cls, name: str, location: Path):
        data = obj_load(location)
        return cls.load_entry_from_obj(name, data)

    @classmethod
    @abc.abstractmethod
    def load_entry_from_obj(cls, name: str, obj: Dict):
        """ Load leaderboard entry from a given object """
        pass

    @classmethod
    def create_from_entry_folder(cls, name: str, location: Path):
        entries = [obj_load(file) for file in location.iterdir()]
        return cls.create_from_entries(name, entries)

    @classmethod
    @abc.abstractmethod
    def create_from_entries(cls, name: str, entries: List[Any]):
        pass

    @staticmethod
    @abc.abstractmethod
    def extract_base_from_entry(entry: Any) -> LeaderboardEntryBase:
        pass

    @staticmethod
    @abc.abstractmethod
    def update_entry_from_base(entry: Any, base: LeaderboardEntryBase):
        pass

    @staticmethod
    @abc.abstractmethod
    def write_entry(entry: Any, file: Path):
        pass

    @abc.abstractmethod
    def export_as_csv(self, file: Path):
        pass

    @abc.abstractmethod
    def export_as_json(self, file: Path):
        pass


class LeaderboardRegistry(PluginRegistry):
    """Registry for leaderboard managers"""

    def __init__(self):
        super().__init__('leaderboards')

    def load(self, name) -> Optional[LeaderboardManager]:
        entry = self._entry(name)
        return self._load_obj(entry)


def list_items():
    """ List registered leaderboard managers """
    reg = LeaderboardRegistry()
    for item in reg.names:
        print(reg.load(item))
