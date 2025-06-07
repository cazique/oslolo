
# tests/test_tui.py
import pytest
from oslolo.tui.app import OsloloTuiApp

@pytest.mark.asyncio
async def test_tui_startup():
    """Test that the TUI app can be instantiated."""
    app = OsloloTuiApp()
    # A simple instantiation test is enough for a basic check
    assert app.title == "OSLolo v1.0 - Norton Commander Mode"
