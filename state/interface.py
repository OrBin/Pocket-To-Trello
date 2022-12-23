import abc
from typing import Optional


class StateManager(abc.ABC):
    @abc.abstractmethod
    def _exists(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def _read(self) -> str:
        raise NotImplementedError()

    def read(self, default: Optional[str] = None) -> str:
        if not self._exists():
            assert default is not None, "Previous state not found, but default was not provided"
            return default
        return self._read()

    @abc.abstractmethod
    def write(self, new_state: str):
        raise NotImplementedError()
