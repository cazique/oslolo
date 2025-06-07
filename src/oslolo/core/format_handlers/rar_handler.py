
# src/oslolo/core/format_handlers/rar_handler.py
import rarfile
from pathlib import Path
from typing import List, Generator
from .base_handler import BaseHandler

class RarHandler(BaseHandler):
    """Handler for RAR archives."""

    def __init__(self):
        # Ensure unrar tool is available
        try:
            rarfile.tool_setup()
        except rarfile.UnrarError as e:
            raise RuntimeError("unrar command not found, please install it to handle RAR files.") from e


    def extract(self, archive_path: Path, dest_path: Path) -> None:
        with rarfile.RarFile(archive_path, 'r') as rf:
            rf.extractall(path=dest_path)

    def list_contents(self, archive_path: Path) -> Generator[str, None, None]:
        with rarfile.RarFile(archive_path, 'r') as rf:
            for name in rf.namelist():
                yield name

    def create(self, archive_path: Path, files: List[Path], base_dir: Path) -> None:
        raise NotImplementedError("Creating RAR archives is not supported due to licensing restrictions.")

    def test_integrity(self, archive_path: Path) -> bool:
        try:
            with rarfile.RarFile(archive_path, 'r') as rf:
                rf.testrar()
                return True
        except Exception:
            return False
