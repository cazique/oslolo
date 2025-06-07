
# src/oslolo/tui/app.py
from textual.app import App
from textual.binding import Binding
from .screens.main_screen import MainScreen

class OsloloTuiApp(App):
    """The main application for the OSLolo TUI mode."""

    CSS_PATH = "themes/norton_classic.tcss"
    TITLE = "OSLolo v1.0 - Norton Commander Mode"
    
    BINDINGS = [
        Binding(key="f10", action="quit", description="Quit"),
        Binding(key="ctrl+c", action="quit", description="Quit"),
    ]

    def on_mount(self) -> None:
        """Called when the app is first mounted."""
        self.push_screen(MainScreen())

    def action_quit(self) -> None:
        """An action to quit the application."""
        self.exit()
