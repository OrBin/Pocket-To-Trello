import abc
from typing import Optional


class StateManager(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def _exists(cls) -> bool:
        raise NotImplementedError()

    @classmethod
    @abc.abstractmethod
    def _read(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def read(cls, default: Optional[str] = None) -> str:
        if not cls._exists():
            assert default is not None, "Previous state not found, but default was not provided"
            return default
        return cls._read()

    @classmethod
    @abc.abstractmethod
    def write(cls, new_state: str):
        raise NotImplementedError()
