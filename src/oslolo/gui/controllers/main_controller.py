
# src/oslolo/gui/controllers/main_controller.py
from PyQt6.QtCore import QObject, pyqtSlot, QRunnable, QThreadPool
from oslolo.core.archive_manager import ArchiveManager

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.fn(*self.args, **self.kwargs)

class MainController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.manager = ArchiveManager()
        self.threadpool = QThreadPool()
        self._connect_signals()

    def _connect_signals(self):
        self.view.tree_widget.files_dropped.connect(self.handle_files_dropped)
        self.view.extract_action.triggered.connect(self.extract_archive)
        
    def handle_files_dropped(self, file_paths):
        if not file_paths:
            return
        
        archive_path = file_paths[0]
        self.open_archive(archive_path)

    def open_archive(self, path):
        self.view.tree_widget.clear()
        self.view.statusBar().showMessage(f"Opening {path}...")
        
        try:
            contents = self.manager.list_contents(path)
            for item in contents:
                self.view.add_tree_item(item)
            self.view.statusBar().showMessage(f"Loaded {path}", 5000)
        except Exception as e:
            self.view.statusBar().showMessage(f"Error opening {path}: {e}", 5000)
            
    def extract_archive(self):
        # In a real app, this would open a file dialog to get destination
        self.view.statusBar().showMessage("Extract action triggered. (Impl. needed)")
