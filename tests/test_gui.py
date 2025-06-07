# tests/test_gui.py
import pytest
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QMimeData, QUrl, Qt, QTimer # Added QMimeData, QUrl, Qt, QTimer
from unittest.mock import patch, MagicMock # Added patch, MagicMock
import time # Added for time.sleep

from oslolo.gui.views.main_window import MainWindow
# If MainController needs to be instantiated directly for some tests:
# from oslolo.gui.controllers.main_controller import MainController

# This needs pytest-qt
@pytest.mark.skipif("not config.getoption('--gui-tests')")
def test_gui_startup(qtbot):
    """Basic test to see if the GUI window starts without errors."""
    app = QApplication.instance() # Ensure QApplication instance exists
    if app is None:
        app = QApplication([])

    window = MainWindow()
    qtbot.addWidget(window)
    
    assert window.windowTitle() == "OSLolo Archive Manager"
    assert window.statusBar().currentMessage().startswith("Ready")

@pytest.mark.skipif("not config.getoption('--gui-tests')")
@patch('oslolo.gui.views.main_window.MainController.open_archive') # Patched at source of MainController for MainWindow
def test_drag_drop_opens_archive(mock_open_archive, qtbot):
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    window = MainWindow()
    qtbot.addWidget(window)
    # window.show() # Not always strictly necessary for qtbot tests if not interacting with visible elements

    test_file_path = "/tmp/test_archive.zip"

    # The DragDropTreeWidget.archive_opened signal is connected to controller.open_archive.
    # Emitting this signal directly tests the connection and subsequent call.
    window.tree_widget.archive_opened.emit(test_file_path)

    # Wait for the mock to be called
    # Increased timeout just in case of slow test environments, though it should be quick
    qtbot.waitUntil(lambda: mock_open_archive.called, timeout=2000)

    mock_open_archive.assert_called_once_with(test_file_path)

@pytest.mark.skipif("not config.getoption('--gui-tests')")
def test_non_blocking_open_archive(qtbot):
    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    window = MainWindow()
    qtbot.addWidget(window)
    # window.show()

    mock_list_contents_result = ["file1.txt", "file2.txt"]
    mocked_list_contents_func = MagicMock()

    def slow_list_contents(*args, **kwargs):
        # This function runs in the ArchiveWorker's thread.
        # time.sleep() will block this worker thread, simulating work.
        # The main GUI thread should remain responsive.
        time.sleep(0.2) # Simulate 200ms of work
        return mock_list_contents_result

    mocked_list_contents_func.side_effect = slow_list_contents

    # Patching 'oslolo.core.archive_manager.ArchiveManager.list_contents'
    # This is the canonical path to the class method.
    with patch('oslolo.core.archive_manager.ArchiveManager.list_contents', new=mocked_list_contents_func):
        test_archive_path = "/tmp/dummy_archive.zip"

        initial_message = window.statusBar().currentMessage()
        assert "Ready" in initial_message or not initial_message # Could be empty initially

        # Trigger the operation
        window.tree_widget.archive_opened.emit(test_archive_path)

        # 1. Check for "Opening..." message (synchronous part of open_archive)
        qtbot.waitUntil(lambda: f"Opening {test_archive_path}..." in window.statusBar().currentMessage(), timeout=1000)

        # 2. Check for "Processing archive..." (first progress signal from worker)
        # This message is set when progress is 0.
        qtbot.waitUntil(lambda: window.statusBar().currentMessage() == "Processing archive...", timeout=1000)

        # 3. Check for "Finalizing..." (progress 100, before finished signal fully handled)
        # This message is set when progress is 100.
        qtbot.waitUntil(lambda: window.statusBar().currentMessage() == "Finalizing archive processing...", timeout=1000)

        # 4. Wait for the final status message indicating success and tree population
        # This is set by _handle_archive_contents after worker emits 'finished'.
        qtbot.waitUntil(
            lambda: f"Archive contents loaded successfully. {len(mock_list_contents_result)} items." in window.statusBar().currentMessage(),
            timeout=3000
        )

        mocked_list_contents_func.assert_called_once_with(test_archive_path)

        assert window.tree_widget.topLevelItemCount() == len(mock_list_contents_result)
        assert window.tree_widget.topLevelItem(0).text(0) == mock_list_contents_result[0]
        assert window.tree_widget.topLevelItem(1).text(0) == mock_list_contents_result[1]
