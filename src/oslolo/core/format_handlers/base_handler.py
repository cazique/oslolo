
# src/oslolo/core/format_handlers/base_handler.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Generator

class BaseHandler(ABC):
    """Abstract base class for all archive format handlers."""

    @abstractmethod
    def extract(self, archive_path: Path, dest_path: Path) -> None:
        """Extracts an archive to a destination path."""
        pass

    @abstractmethod
    def list_contents(self, archive_path: Path) -> Generator[str, None, None]:
        """Lists the contents of an archive."""
        pass

    @abstractmethod
    def create(self, archive_path: Path, files: List[Path], base_dir: Path) -> None:
        """Creates an archive from a list of files."""
        pass

    @abstractmethod
    def test_integrity(self, archive_path: Path) -> bool:
        """Tests the integrity of an archive."""
        pass
