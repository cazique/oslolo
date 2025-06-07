
# src/oslolo/tui/screens/main_screen.py
from textual.screen import Screen
from textual.app import ComposeResult
from ..widgets.dual_panel import DualPanel
from ..widgets.command_bar import CommandBar

class MainScreen(Screen):
    """The main dual-panel screen for the TUI."""

    def compose(self) -> ComposeResult:
        yield DualPanel()
        yield CommandBar()
