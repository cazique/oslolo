
# src/oslolo/core/format_handlers/tar_handler.py
import tarfile
from pathlib import Path
from typing import List, Generator
from .base_handler import BaseHandler

class TarHandler(BaseHandler):
    """Handler for TAR, TAR.GZ, TAR.BZ2, TAR.XZ archives."""

    def _get_mode(self, archive_path: Path) -> str:
        suffixes = ''.join(archive_path.suffixes).lower()
        if suffixes.endswith('.tar.gz') or suffixes.endswith('.tgz'):
            return 'r:gz'
        if suffixes.endswith('.tar.bz2') or suffixes.endswith('.tbz2'):
            return 'r:bz2'
        if suffixes.endswith('.tar.xz') or suffixes.endswith('.txz'):
            return 'r:xz'
        return 'r:'

    def _get_write_mode(self, archive_path: Path) -> str:
        return self._get_mode(archive_path).replace('r', 'w', 1)

    def extract(self, archive_path: Path, dest_path: Path) -> None:
        with tarfile.open(archive_path, self._get_mode(archive_path)) as tf:
            tf.extractall(path=dest_path)

    def list_contents(self, archive_path: Path) -> Generator[str, None, None]:
        with tarfile.open(archive_path, self._get_mode(archive_path)) as tf:
            for member in tf.getmembers():
                yield member.name

    def create(self, archive_path: Path, files: List[Path], base_dir: Path) -> None:
        with tarfile.open(archive_path, self._get_write_mode(archive_path)) as tf:
            for file_path in files:
                tf.add(file_path, arcname=file_path.relative_to(base_dir))

    def test_integrity(self, archive_path: Path) -> bool:
        # Tarfile doesn't have a direct test method. Reading all members is a proxy.
        try:
            with tarfile.open(archive_path, self._get_mode(archive_path)) as tf:
                for member in tf:
                    if member.issym() or member.islnk():
                        continue
                    if member.isfile():
                        tf.extractfile(member).read()
            return True
        except Exception:
            return False
