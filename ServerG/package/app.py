from PyQt6.QtWidgets import QApplication
from package.mainwindow import MainWindow
import qdarktheme
import sys

def run():
    app = QApplication(sys.argv)
    qdarktheme.load_stylesheet("dark")
    window = MainWindow()
  
    app.exec()