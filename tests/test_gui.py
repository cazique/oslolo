
# tests/test_gui.py
import pytest
from PyQt6.QtWidgets import QApplication
from oslolo.gui.views.main_window import MainWindow

# This needs pytest-qt
@pytest.mark.skipif("not config.getoption('--gui-tests')")
def test_gui_startup(qtbot):
    """Basic test to see if the GUI window starts without errors."""
    window = MainWindow()
    qtbot.addWidget(window)
    
    assert window.windowTitle() == "OSLolo Archive Manager"
    assert window.statusBar().currentMessage().startswith("Ready")
