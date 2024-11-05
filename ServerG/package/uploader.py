from PyQt6.QtWidgets import QDialog
from PyQt6.QtCore import QThread, pyqtSignal
from package.ui import errordialog_ui
import rust_modules
import time

class Uploader(QThread):
    error = pyqtSignal()
    
    def run(self):
        if rust_modules.is_dir_empty(".\\server"):    
            self.error.emit()
        else:
            rust_modules.upload_server()