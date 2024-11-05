from PyQt6.QtCore import QThread
import rust_modules

class Downloader(QThread):
    def run(self):
        if rust_modules.is_dir_empty(".\\server"):
            rust_modules.download_create_server()
        else:
            rust_modules.download_update_server()