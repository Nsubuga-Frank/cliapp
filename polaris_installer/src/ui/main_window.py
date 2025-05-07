# src/ui/main_window.py - updated with thread cleanup
import os

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QFontDatabase, QIcon
from PySide6.QtWidgets import (QHBoxLayout, QMainWindow, QPushButton,
                               QTabWidget, QVBoxLayout, QWidget, QMessageBox)
from src.ui.tabs.about import AboutTab
from src.ui.tabs.general import GeneralTab
from src.ui.tabs.installer import InstallerTab
from src.ui.tabs.settings import SettingsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Set up window properties
        self.setWindowTitle("Polaris Installer Properties")
        self.setFixedSize(500, 520)
        self.setWindowIcon(QIcon(os.path.join("resources", "images", "logo.png")))
        
        # Initialize installation settings
        self.installation_settings = {
            "install_dir": os.path.expanduser("~/Polaris") if os.name != "nt" else "C:\\Program Files\\Polaris",
            "python_version": "system",
            "create_shortcut": True,
            "add_to_path": True,
            "launch_on_startup": False
        }
        
        # Load custom fonts and styles
        self._setup_styles()
        
        # Create main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.main_layout.addWidget(self.tab_widget)
        
        # Add tabs
        self.general_tab = GeneralTab()
        self.settings_tab = SettingsTab()
        self.installer_tab = InstallerTab()
        self.about_tab = AboutTab()
        
        self.tab_widget.addTab(self.general_tab, "General")
        self.tab_widget.addTab(self.settings_tab, "Settings")
        self.tab_widget.addTab(self.installer_tab, "Installer")
        self.tab_widget.addTab(self.about_tab, "About")
        
        # Connect signals
        self.settings_tab.settings_updated.connect(self.update_installer_settings)
        self.connect_installer_tab()
        
        # Set default tab
        self.tab_widget.setCurrentIndex(2)  # Installer tab
        
        # Bottom action bar
        self.bottom_widget = QWidget()
        self.bottom_layout = QHBoxLayout(self.bottom_widget)
        self.bottom_layout.setContentsMargins(10, 5, 10, 5)
        
        # Add bottom spacer and Cancel button
        self.bottom_layout.addStretch()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        self.bottom_layout.addWidget(self.cancel_button)
        
        self.main_layout.addWidget(self.bottom_widget)
    
    def _setup_styles(self):
        # Load custom fonts if needed
        # QFontDatabase.addApplicationFont(os.path.join("resources", "fonts", "custom_font.ttf"))
        
        # Load and apply stylesheet
        style_path = os.path.join("src", "ui", "resources", "styles.qss")
        if os.path.exists(style_path):
            with open(style_path, "r") as f:
                self.setStyleSheet(f.read())
    
    def update_installer_settings(self, settings):
        """Update installer settings when they change in the settings tab"""
        self.installation_settings.update(settings)
        
        # If installer tab is initialized, update its settings
        if hasattr(self.installer_tab, 'update_settings'):
            self.installer_tab.update_settings(self.installation_settings)
    
    def connect_installer_tab(self):
        """Connect signals from installer tab if applicable"""
        # Connect start installation signal if available
        if hasattr(self.installer_tab, 'start_installation_requested'):
            self.installer_tab.start_installation_requested.connect(
                lambda: self.start_installation(self.installation_settings)
            )
    
    def start_installation(self, settings):
        """Start the installation process with the current settings"""
        # Create installation process with current settings
        if hasattr(self.installer_tab, 'start_installation'):
            self.installer_tab.start_installation(settings)
    
    def closeEvent(self, event):
        """Handle window close event - ensure threads are properly terminated"""
        # Check if installation thread is running and clean it up
        if hasattr(self.installer_tab, 'installation') and self.installer_tab.installation:
            # Check if the thread is running
            if self.installer_tab.installation.isRunning():
                # Ask user confirmation before closing
                reply = QMessageBox.question(
                    self, 
                    "Polaris Installer", 
                    "Installation is still in progress. Are you sure you want to exit?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    # Tell the thread to abort
                    if hasattr(self.installer_tab.installation, 'abort'):
                        self.installer_tab.installation.abort = True
                    
                    # Wait for the thread to finish with a timeout
                    if not self.installer_tab.installation.wait(2000):  # 2 second timeout
                        # Force termination if still running
                        self.installer_tab.installation.terminate()
                        self.installer_tab.installation.wait()  # Wait for actual termination
                    
                    # Accept the close event
                    event.accept()
                else:
                    # Reject the close event if user cancels
                    event.ignore()
            else:
                # Thread is not running, accept the close event
                event.accept()
        else:
            # No thread running, accept the close event
            event.accept()