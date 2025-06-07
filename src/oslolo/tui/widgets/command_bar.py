
# src/oslolo/tui/widgets/command_bar.py
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Label

class CommandBar(Widget):
    """A footer-like bar showing F-key commands."""

    COMMANDS = {
        "F1": "Help", "F3": "View", "F4": "Edit", "F5": "Copy",
        "F6": "Move", "F7": "Mkdir", "F8": "Del", "F10": "Quit"
    }

    def compose(self) -> ComposeResult:
        for key, desc in self.COMMANDS.items():
            yield Label(key, classes="key")
            yield Label(f"{desc}")
