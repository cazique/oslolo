
# src/oslolo/gui/controllers/main_controller.py
from PyQt6.QtCore import QObject, pyqtSlot, QRunnable, QThreadPool, pyqtSignal
from oslolo.core.archive_manager import ArchiveManager
# from PyQt6.QtWidgets import QMessageBox # Keep commented for now

class WorkerSignals(QObject):
    finished = pyqtSignal(object)  # Emits the result of the operation
    error = pyqtSignal(str)       # Emits an error message if an exception occurs
    progress = pyqtSignal(int)    # Emits progress percentage (0-100)

class ArchiveWorker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()  # Decorator for methods intended to be invoked by Qt's meta-object system (though QRunnable.run is special)
    def run(self):
        try:
            self.signals.progress.emit(0)  # Signal start of operation
            result = self.fn(*self.args, **self.kwargs)
            self.signals.progress.emit(100) # Signal end of operation (successful path)
            self.signals.finished.emit(result)
        except Exception as e:
            self.signals.error.emit(str(e))
            # Optionally: self.signals.progress.emit(100) # To ensure progress always completes

class MainController(QObject):
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.manager = ArchiveManager()
        self.threadpool = QThreadPool()
        print(f"Max threads for controller: {self.threadpool.maxThreadCount()}") # For debugging
        self._connect_signals()

    def _connect_signals(self):
        # The connection for files_dropped is now handled by MainWindow connecting
        # tree_widget.archive_opened to self.open_archive.
        # So, we can remove/comment out the old connection here:
        # self.view.tree_widget.files_dropped.connect(self.handle_files_dropped) # Commented out
        
        # The extract_action connection remains commented as per previous step
        # self.view.extract_action.triggered.connect(self.extract_archive)
        pass # No connections needed from controller to view's tree_widget.files_dropped anymore for this use case

    # handle_files_dropped can be removed or kept if files_dropped signal has other uses.
    # For now, let's comment it out to ensure it's not accidentally used for opening.
    # def handle_files_dropped(self, file_paths):
    #     if not file_paths:
    #         return
    #     archive_path = file_paths[0]
    #     self.open_archive(archive_path) # This logic is now directly triggered by MainWindow

    def open_archive(self, path): # This method is now directly called by signal from MainWindow
        self.view.tree_widget.clear()
        self.view.statusBar().showMessage(f"Opening {path}...")

        worker = ArchiveWorker(self.manager.list_contents, path)
        worker.signals.finished.connect(self._handle_archive_contents)
        worker.signals.error.connect(self._handle_archive_error)
        worker.signals.progress.connect(self._handle_archive_progress)
        
        self.threadpool.start(worker)

    def _handle_archive_contents(self, contents):
        if contents is None:
            self.view.statusBar().showMessage("Archive is empty or contents could not be listed.", 5000)
            return

        if not contents:
            self.view.statusBar().showMessage(f"Archive opened successfully. No files found inside.", 5000)
            return

        for item_name in contents:
            self.view.add_tree_item(item_name)

        self.view.statusBar().showMessage(f"Archive contents loaded successfully. {len(contents)} items.", 5000)

    def _handle_archive_error(self, error_message):
        self.view.statusBar().showMessage(f"Error: {error_message}", 10000)
        # from PyQt6.QtWidgets import QMessageBox
        # QMessageBox.critical(self.view, "Error Opening Archive", f"An error occurred: {error_message}")

    def _handle_archive_progress(self, percent):
        if percent == 0:
            self.view.statusBar().showMessage("Processing archive...")
        elif percent == 100:
            self.view.statusBar().showMessage("Finalizing archive processing...", 2000)
        # else:
            # self.view.statusBar().showMessage(f"Processing archive... {percent}% complete")

    def extract_archive(self):
        self.view.statusBar().showMessage("Extract action triggered. (Implementation with threading needed)")
