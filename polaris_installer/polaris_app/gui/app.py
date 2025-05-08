# gui/app.py
from PySide6.QtWidgets import QMainWindow, QTabWidget
from PySide6.QtGui import QIcon
import os

# Import views
from gui.views.dashboard import DashboardView
from gui.views.settings import SettingsView
from gui.views.about import AboutView

class PolarisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MINER NODE")
        self.setMinimumSize(680, 480)  # Reduced window size
        self.resize(720, 520)  # Set initial window size
        
        # Set window icon if available
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                               "resources", "images", "logo.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Create the dashboard as the central widget (no tabs in this version)
        self.dashboard = DashboardView()
        self.setCentralWidget(self.dashboard)