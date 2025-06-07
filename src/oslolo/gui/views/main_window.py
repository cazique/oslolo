
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
        self.setup_ui() # Sets up self.tree_widget
        self.setup_menus_and_toolbar()
        self.controller = MainController(self) # Controller gets a reference to the main window (view)
        self._connect_signals() # New method to connect view signals to controller slots

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

    def add_tree_item(self, name): # name, size, modified
        # This method should be robust. If list_contents provides more data, adapt here.
        # For now, assuming 'name' is a string.
        item = QTreeWidgetItem([str(name), "", ""]) # Ensure name is string for display
        self.tree_widget.addTopLevelItem(item)

    def _connect_signals(self):
        # Connect the new signal from DragDropTreeWidget to the controller's method
        self.tree_widget.archive_opened.connect(self.controller.open_archive)

        # The controller will now directly receive the path to open.
        # The old self.view.tree_widget.files_dropped.connect(self.handle_files_dropped)
        # in MainController can be removed if this new signal is the primary way to open archives.
        # Let's defer removing it from MainController until we confirm this new path works well.

# run_standalone_gui and if __name__ == '__main__' remains the same
def run_standalone_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    run_standalone_gui()
