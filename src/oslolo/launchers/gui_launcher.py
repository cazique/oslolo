
# src/oslolo/launchers/gui_launcher.py
import sys
from PyQt6.QtWidgets import QApplication
import qdarkstyle
from oslolo.gui.views.main_window import MainWindow

def run_gui(archive_path: str = None):
    """Initializes and runs the PyQt6 GUI application."""
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt6'))
    
    window = MainWindow()
    if archive_path:
        window.controller.open_archive(archive_path)
        
    window.show()
    sys.exit(app.exec())
