import abc
from logging import Logger
from typing import Optional


class StateManager(abc.ABC):
    def __init__(self, logger: Logger):
        self._logger = logger

    @abc.abstractmethod
    def _exists(self) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def _read(self) -> str:
        raise NotImplementedError()

    def read(self, default: Optional[str] = None) -> str:
        if not self._exists():
            self._logger.info("Previous state not found, defaulting to '%s'", default)
            assert default is not None, "Previous state not found, but default was not provided"
            return default

        state = self._read()
        self._logger.info("Read previous state: '%s'", state)
        return state

    @abc.abstractmethod
    def _write(self, new_state: str):
        raise NotImplementedError()

    def write(self, new_state: str):
        self._logger.info("Writing new state: '%s'", new_state)
        self._write(new_state)
