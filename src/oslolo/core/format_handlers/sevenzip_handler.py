
# src/oslolo/core/format_handlers/sevenzip_handler.py
import py7zr
from pathlib import Path
from typing import List, Generator
from .base_handler import BaseHandler

class SevenZipHandler(BaseHandler):
    """Handler for 7Z archives."""

    def extract(self, archive_path: Path, dest_path: Path) -> None:
        with py7zr.SevenZipFile(archive_path, 'r') as szf:
            szf.extractall(path=dest_path)

    def list_contents(self, archive_path: Path) -> Generator[str, None, None]:
        with py7zr.SevenZipFile(archive_path, 'r') as szf:
            for name in szf.getnames():
                yield name

    def create(self, archive_path: Path, files: List[Path], base_dir: Path) -> None:
        with py7zr.SevenZipFile(archive_path, 'w') as szf:
            for file_path in files:
                szf.write(file_path, arcname=file_path.relative_to(base_dir))

    def test_integrity(self, archive_path: Path) -> bool:
        try:
            with py7zr.SevenZipFile(archive_path, 'r') as szf:
                return szf.test()
        except Exception:
            return False
