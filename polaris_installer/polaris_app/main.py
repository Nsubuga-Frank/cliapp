#!/usr/bin/env python3
import sys
import os

# Force Qt to use X11 backend instead of Wayland
os.environ["QT_QPA_PLATFORM"] = "xcb"

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QDir
from PySide6.QtGui import QIcon

# Import local modules
from gui.app import PolarisApp

def setup_environment():
    """Set up the application environment"""
    # Set the working directory to this file's location
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create resources directory if it doesn't exist
    os.makedirs(os.path.join("resources", "images", "icons"), exist_ok=True)
    os.makedirs(os.path.join("resources", "images", "networks"), exist_ok=True)
    os.makedirs(os.path.join("resources", "styles"), exist_ok=True)

if __name__ == "__main__":
    # Set up the environment
    setup_environment()
    
    # Create the Qt application
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle("Fusion")
    
    # Set application icon if available
    icon_path = os.path.join("resources", "images", "logo.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Create and show the main window
    polaris = PolarisApp()
    polaris.show()
    
    # Execute the application
    sys.exit(app.exec())