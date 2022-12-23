from typing import Type

from state.interface import StateManager
from state.local_file import LocalFileStateManager


def select_state_manager() -> Type[StateManager]:
    return LocalFileStateManager
