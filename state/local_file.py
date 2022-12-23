from pathlib import Path

from state.interface import StateManager


STATE_PATH = Path(__file__).parent.parent / "pocket_last_checked.txt"


class LocalFileStateManager(StateManager):
    def _exists(self) -> bool:
        return STATE_PATH.exists()

    def _read(self) -> str:
        return STATE_PATH.read_text()

    def _write(self, new_state: str):
        STATE_PATH.write_text(new_state)
