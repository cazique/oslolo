
# src/oslolo/core/archive_manager.py
import logging
from pathlib import Path
from typing import List, Generator
from .compression_engine import CompressionEngine

logger = logging.getLogger(__name__)

class ArchiveManager:
    """
    High-level API for managing archive files.
    This is the primary interface for all UIs (GUI, TUI, CLI).
    """

    def __init__(self):
        """Initializes the ArchiveManager with a CompressionEngine."""
        self.engine = CompressionEngine()

    def extract(self, archive_path: str, dest_path: str) -> None:
        """Extracts an archive to a destination directory."""
        logger.info(f"Attempting to extract '{archive_path}' to '{dest_path}'")
        try:
            archive = Path(archive_path).resolve()
            destination = Path(dest_path).resolve()
            destination.mkdir(parents=True, exist_ok=True)
            self.engine.extract(archive, destination)
            logger.info(f"Successfully extracted '{archive_path}'")
        except Exception as e:
            logger.error(f"Extraction failed for '{archive_path}': {e}", exc_info=True)
            raise

    def create(self, archive_path: str, file_paths: List[str], format: str = 'zip') -> None:
        """Creates a new archive from a list of files and/or directories."""
        logger.info(f"Attempting to create '{archive_path}' from {len(file_paths)} sources.")
        try:
            archive = Path(archive_path).resolve()
            
            all_files = []
            for p_str in file_paths:
                p = Path(p_str)
                if p.is_dir():
                    all_files.extend(list(p.rglob("*")))
                elif p.is_file():
                    all_files.append(p)
            
            resolved_files = [f.resolve() for f in all_files if f.is_file()]
            self.engine.create(archive, resolved_files, format)
            logger.info(f"Successfully created '{archive_path}'")
        except Exception as e:
            logger.error(f"Creation failed for '{archive_path}': {e}", exc_info=True)
            raise

    def list_contents(self, archive_path: str) -> Generator[str, None, None]:
        """Lists the contents of an archive."""
        logger.info(f"Listing contents of '{archive_path}'")
        try:
            archive = Path(archive_path).resolve()
            return self.engine.list_contents(archive)
        except Exception as e:
            logger.error(f"Failed to list contents of '{archive_path}': {e}", exc_info=True)
            raise

    def test_integrity(self, archive_path: str) -> bool:
        """Tests the integrity of an archive."""
        logger.info(f"Testing integrity of '{archive_path}'")
        try:
            archive = Path(archive_path).resolve()
            result = self.engine.test_integrity(archive)
            logger.info(f"Integrity test for '{archive_path}': {'OK' if result else 'Failed'}")
            return result
        except Exception as e:
            logger.error(f"Integrity test failed for '{archive_path}': {e}", exc_info=True)
            return False
