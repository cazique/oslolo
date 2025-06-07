# src/oslolo/core/compression_engine.py
import logging
import os
from pathlib import Path
from typing import List, Generator

from .format_detector import detect_format
from .format_handlers import get_handler

logger = logging.getLogger(__name__)

class CompressionEngine:
    """Orchestrates compression and extraction operations."""

    def _get_handler(self, archive_path: Path, format_override: str = None):
        format_name = format_override or detect_format(archive_path)
        if not format_name:
            raise ValueError(f"Could not determine format for {archive_path}")
        logger.info(f"Using handler '{format_name}' for {archive_path}")
        return get_handler(format_name)

    def extract(self, archive_path: Path, dest_path: Path) -> None:
        handler = self._get_handler(archive_path)
        handler.extract(archive_path, dest_path)

    def create(self, archive_path: Path, files: List[Path], format: str) -> None:
        handler = self._get_handler(archive_path, format_override=format)
        
        # Determinar un directorio base común usando os.path.commonpath
        if not files:
            raise ValueError("No files provided for archive creation.")
        
        # Convertir a strings para usar commonpath
        file_paths_str = [str(f.resolve()) for f in files]
        
        try:
            # Usar el directorio común de todos los archivos
            common_base_str = os.path.commonpath(file_paths_str)
            common_base = Path(common_base_str)
            
            # Si el directorio común es un archivo, usar su parent
            if common_base.is_file():
                common_base = common_base.parent
                
        except ValueError:
            # Si no hay directorio común (ej: archivos en diferentes drives en Windows)
            # Usar el directorio de trabajo actual
            common_base = Path.cwd()

        logger.info(f"Using common base directory: {common_base}")
        handler.create(archive_path, files, common_base)

    def list_contents(self, archive_path: Path) -> Generator[str, None, None]:
        handler = self._get_handler(archive_path)
        return handler.list_contents(archive_path)

    def test_integrity(self, archive_path: Path) -> bool:
        handler = self._get_handler(archive_path)
        return handler.test_integrity(archive_path)
