
# src/oslolo/core/format_handlers/zip_handler.py
import zipfile
from pathlib import Path
from typing import List, Generator
from .base_handler import BaseHandler

class ZipHandler(BaseHandler):
    """Handler for ZIP archives."""

    def extract(self, archive_path: Path, dest_path: Path) -> None:
        with zipfile.ZipFile(archive_path, 'r') as zf:
            zf.extractall(path=dest_path)

    def list_contents(self, archive_path: Path) -> Generator[str, None, None]:
        with zipfile.ZipFile(archive_path, 'r') as zf:
            for name in zf.namelist():
                yield name

    def create(self, archive_path: Path, files: List[Path], base_dir: Path) -> None:
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in files:
                zf.write(file_path, arcname=file_path.relative_to(base_dir))

    def test_integrity(self, archive_path: Path) -> bool:
        try:
            with zipfile.ZipFile(archive_path, 'r') as zf:
                return zf.testzip() is None
        except zipfile.BadZipFile:
            return False
