# src/installer.py
import sys

from PySide6.QtWidgets import QApplication
from src.ui.main_window import MainWindow


class PolarisInstaller:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
    
    def run(self):
        self.window.show()
        return self.app.exec()