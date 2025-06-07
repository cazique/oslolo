# src/oslolo/core/format_detector.py
from pathlib import Path

FORMAT_HANDLERS = {
    '.7z': 'sevenzip',
    '.zip': 'zip',
    '.rar': 'rar',
    '.tar': 'tar',
    '.gz': 'tar',
    '.bz2': 'tar',
    '.xz': 'tar',
}

def detect_format(archive_path) -> str | None:
    """Detects archive format based on file extension."""
    # Convertir a Path si es string
    if isinstance(archive_path, str):
        archive_path = Path(archive_path)
    
    suffix = archive_path.suffix.lower()
    if suffix in FORMAT_HANDLERS:
        return FORMAT_HANDLERS[suffix]
    
    # Fallback for complex extensions like .tar.gz
    if ''.join(archive_path.suffixes).lower().startswith('.tar.'):
        return 'tar'
        
    return None
