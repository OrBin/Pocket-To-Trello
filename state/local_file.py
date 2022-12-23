from pathlib import Path

from state.interface import StateManager


STATE_PATH = Path(__file__).parent.parent / "pocket_last_checked.txt"


class LocalFileStateManager(StateManager):
    @classmethod
    def _exists(cls) -> bool:
        return STATE_PATH.exists()

    @classmethod
    def _read(cls) -> str:
        return STATE_PATH.read_text()

    @classmethod
    def write(cls, new_state: str):
        STATE_PATH.write_text(new_state)
