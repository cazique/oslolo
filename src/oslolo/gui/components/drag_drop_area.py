# src/oslolo/gui/components/drag_drop_area.py
from PyQt6.QtWidgets import QTreeWidget
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QDragMoveEvent

class DragDropTreeWidget(QTreeWidget):
    files_dropped = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
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
            event.setDropAction(Qt.DropAction.CopyAction)
            event.accept()
            links = [url.toLocalFile() for url in event.mimeData().urls()]
            self.files_dropped.emit(links)
        else:
            event.ignore()
