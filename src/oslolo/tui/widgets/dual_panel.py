
# src/oslolo/tui/widgets/dual_panel.py
from pathlib import Path
from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Static
from .file_browser import FileBrowser

class DualPanel(Horizontal):
    """A widget containing two file browsers side-by-side."""

    def compose(self) -> ComposeResult:
        home_path = Path.home()
        with Vertical(id="left-panel"):
            yield Static(str(home_path), classes="panel-title")
            yield FileBrowser(path=home_path, id="left_browser")
        
        with Vertical(id="right-panel"):
            yield Static(str(Path.cwd()), classes="panel-title")
            yield FileBrowser(path=Path.cwd(), id="right_browser")
