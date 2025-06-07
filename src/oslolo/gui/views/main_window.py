
# src/oslolo/gui/views/main_window.py
import sys
from PyQt6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QStatusBar,
                             QApplication, QTreeWidgetItem)
from PyQt6.QtGui import QAction, QIcon
import qtawesome as qta
from ..components.drag_drop_area import DragDropTreeWidget
from ..controllers.main_controller import MainController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OSLolo Archive Manager")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()
        self.setup_menus_and_toolbar()
        self.controller = MainController(self)
        
    def setup_ui(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tree_widget = DragDropTreeWidget()
        self.tree_widget.setHeaderLabels(["Name", "Size", "Modified"])
        self.layout.addWidget(self.tree_widget)
        
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("Ready. Drag and drop an archive to open.")

    def setup_menus_and_toolbar(self):
        self.add_action = QAction(qta.icon('fa5s.plus', color='green'), "Add", self)
        self.extract_action = QAction(qta.icon('fa5s.folder-open', color='blue'), "Extract", self)
        self.test_action = QAction(qta.icon('fa5s.check-circle', color='orange'), "Test", self)
        
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.addAction(self.add_action)
        toolbar.addAction(self.extract_action)
        toolbar.addAction(self.test_action)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.extract_action)
        file_menu.addSeparator()
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("About", self)
        help_menu.addAction(about_action)

    def add_tree_item(self, name):
        item = QTreeWidgetItem([name, "", ""])
        self.tree_widget.addTopLevelItem(item)

def run_standalone_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    run_standalone_gui()
