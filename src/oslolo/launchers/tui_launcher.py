
# src/oslolo/launchers/tui_launcher.py
from oslolo.tui.app import OsloloTuiApp

def run_tui():
    """Initializes and runs the Textual TUI application."""
    app = OsloloTuiApp()
    app.run()
