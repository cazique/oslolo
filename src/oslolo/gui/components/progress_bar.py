
# src/oslolo/gui/components/progress_bar.py
from PyQt6.QtWidgets import QProgressDialog
from PyQt6.QtCore import Qt

class OperationProgressDialog(QProgressDialog):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.WindowModality.WindowModal)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self.setAutoClose(True)
        self.setAutoReset(True)
        self.setCancelButton(None)
