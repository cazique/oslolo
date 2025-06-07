# src/oslolo/gui/components/drag_drop_area.py
from PyQt6.QtWidgets import QTreeWidget
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QDragMoveEvent

class DragDropTreeWidget(QTreeWidget):
    files_dropped = pyqtSignal(list)  # Existing signal
    archive_opened = pyqtSignal(str) # New signal for when an archive is dropped to be opened

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        # self.setDragEnabled(True) # This allows dragging items *from* the tree. Keep if needed, or remove if only drop is desired.
                                 # For an archive view, dragging *out* (extracting) is a feature, so keep True.
        self.setDragEnabled(True)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dragMoveEvent(self, event: QDragMoveEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.DropAction.CopyAction) # Indicate the action
            event.accept() # Accept the drop event itself

            urls = event.mimeData().urls()
            local_files = [url.toLocalFile() for url in urls if url.isLocalFile()]

            if local_files:
                # Emit the new signal for the first file, assuming it's an archive to be opened.
                # Future: Add logic to check if it's a recognized archive type.
                self.archive_opened.emit(local_files[0])

                # Emit the existing signal with all dropped files.
                self.files_dropped.emit(local_files)
            else:
                # Handle non-local files if necessary, or ignore
                event.ignore()
        else:
            event.ignore()
