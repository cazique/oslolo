
# src/oslolo/tui/widgets/file_browser.py
import os
from pathlib import Path
from textual.widgets import DirectoryTree
from textual.app import log

class FileBrowser(DirectoryTree):
    """A custom directory tree for Browse files."""
    
    def __init__(self, path: Path, id: str | None = None) -> None:
        super().__init__(str(path), id=id)

    def filter_paths(self, paths: list[Path]) -> list[Path]:
        """Filter out hidden files and directories."""
        return sorted(
            [path for path in paths if not path.name.startswith('.')],
            key=lambda path: (not path.is_dir(), path.name.lower())
        )
