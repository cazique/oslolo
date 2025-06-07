
# src/oslolo/core/format_handlers/__init__.py
from .base_handler import BaseHandler
from .zip_handler import ZipHandler
from .rar_handler import RarHandler
from .sevenzip_handler import SevenZipHandler
from .tar_handler import TarHandler

HANDLERS = {
    'zip': ZipHandler,
    'rar': RarHandler,
    'sevenzip': SevenZipHandler,
    'tar': TarHandler,
}

def get_handler(format_name: str) -> BaseHandler:
    """Gets a handler instance for a given format name."""
    handler_class = HANDLERS.get(format_name)
    if not handler_class:
        raise ValueError(f"Unsupported format: {format_name}")
    return handler_class()
