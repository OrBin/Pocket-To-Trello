from state.interface import StateManager
from state.local_file import LocalFileStateManager


def select_state_manager() -> StateManager:
    return LocalFileStateManager()
