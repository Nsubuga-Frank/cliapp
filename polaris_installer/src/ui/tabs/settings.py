# src/ui/tabs/settings.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QComboBox, QCheckBox,
                             QFileDialog)
from PySide6.QtCore import Signal
import sys
import os
import subprocess

class SettingsTab(QWidget):
    # Signals to update installation settings
    settings_updated = Signal(dict)
    
    def __init__(self):
        super().__init__()
        
        # Default settings
        self.settings = {
            "install_dir": "C:\\Program Files\\Polaris" if os.name == "nt" else os.path.expanduser("~/Polaris"),
            "python_version": "system",
            "create_shortcut": True,
            "add_to_path": True,
            "launch_on_startup": False
        }
        
        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Installation Directory
        self.layout.addWidget(QLabel("Installation Directory"))
        
        dir_layout = QHBoxLayout()
        self.dir_input = QLineEdit(self.settings["install_dir"])
        self.dir_input.textChanged.connect(self.update_install_dir)
        
        browse_button = QPushButton("Browse...")
        browse_button.setFixedWidth(80)
        browse_button.clicked.connect(self.browse_directory)
        
        dir_layout.addWidget(self.dir_input)
        dir_layout.addWidget(browse_button)
        
        self.layout.addLayout(dir_layout)
        self.layout.addSpacing(10)
        
        # Python Version
        self.layout.addWidget(QLabel("Python Version"))
        
        self.python_combo = QComboBox()
        self.populate_python_versions()
        self.python_combo.currentIndexChanged.connect(self.update_python_version)
        
        self.layout.addWidget(self.python_combo)
        self.layout.addSpacing(10)
        
        # Checkboxes
        self.desktop_checkbox = QCheckBox("Create Desktop Shortcut")
        self.desktop_checkbox.setChecked(self.settings["create_shortcut"])
        self.desktop_checkbox.toggled.connect(self.update_create_shortcut)
        self.layout.addWidget(self.desktop_checkbox)
        
        self.path_checkbox = QCheckBox("Add to PATH")
        self.path_checkbox.setChecked(self.settings["add_to_path"])
        self.path_checkbox.toggled.connect(self.update_add_to_path)
        self.layout.addWidget(self.path_checkbox)
        
        self.startup_checkbox = QCheckBox("Launch on startup")
        self.startup_checkbox.setChecked(self.settings["launch_on_startup"])
        self.startup_checkbox.toggled.connect(self.update_launch_on_startup)
        self.layout.addWidget(self.startup_checkbox)
        
        # Ensure the layout expands properly
        self.layout.addStretch()
    
    def browse_directory(self):
        """Open file dialog to select installation directory"""
        directory = QFileDialog.getExistingDirectory(
            self, 
            "Select Installation Directory",
            self.dir_input.text()
        )
        if directory:
            self.dir_input.setText(directory)
            self.settings["install_dir"] = directory
            self.settings_updated.emit(self.settings)
    
    def update_install_dir(self, text):
        """Update install_dir setting when text is changed"""
        self.settings["install_dir"] = text
        self.settings_updated.emit(self.settings)
    
    def update_python_version(self, index):
        """Update python_version setting when selection changes"""
        self.settings["python_version"] = self.python_combo.currentData()
        self.settings_updated.emit(self.settings)
    
    def update_create_shortcut(self, checked):
        """Update create_shortcut setting when checkbox changes"""
        self.settings["create_shortcut"] = checked
        self.settings_updated.emit(self.settings)
    
    def update_add_to_path(self, checked):
        """Update add_to_path setting when checkbox changes"""
        self.settings["add_to_path"] = checked
        self.settings_updated.emit(self.settings)
    
    def update_launch_on_startup(self, checked):
        """Update launch_on_startup setting when checkbox changes"""
        self.settings["launch_on_startup"] = checked
        self.settings_updated.emit(self.settings)
    
    def populate_python_versions(self):
        """Find available Python versions on the system"""
        # Clear existing items
        self.python_combo.clear()
        
        # Add system Python
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        self.python_combo.addItem(f"Use System Python ({py_version})", "system")
        
        # Try to find other Python versions (this is platform-specific)
        try:
            if os.name == "nt":  # Windows
                # Check common Python installation locations
                for version in ["3.7", "3.8", "3.9", "3.10", "3.11", "3.12"]:
                    for path in [
                        f"C:\\Python{version.replace('.', '')}\\python.exe",
                        f"C:\\Program Files\\Python{version.replace('.', '')}\\python.exe",
                        f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Programs\\Python\\Python{version.replace('.', '')}\\python.exe"
                    ]:
                        if os.path.exists(path):
                            # Get exact version
                            try:
                                result = subprocess.run(
                                    [path, "--version"], 
                                    capture_output=True, 
                                    text=True,
                                    timeout=1
                                )
                                if result.stdout:
                                    version_text = result.stdout.strip()
                                else:
                                    version_text = result.stderr.strip()
                                
                                if version_text.startswith("Python "):
                                    exact_version = version_text.split(" ")[1]
                                    self.python_combo.addItem(f"Python {exact_version} ({path})", path)
                            except:
                                # If error, just add with the expected version
                                self.python_combo.addItem(f"Python {version} ({path})", path)
            else:  # Unix/Linux/macOS
                # Check common Python installation locations
                for version in ["python3.7", "python3.8", "python3.9", "python3.10", "python3.11", "python3.12"]:
                    try:
                        # Check if this Python version exists in PATH
                        result = subprocess.run(
                            ["which", version], 
                            capture_output=True, 
                            text=True,
                            timeout=1
                        )
                        if result.returncode == 0 and result.stdout.strip():
                            path = result.stdout.strip()
                            # Get exact version
                            try:
                                version_result = subprocess.run(
                                    [path, "--version"], 
                                    capture_output=True, 
                                    text=True,
                                    timeout=1
                                )
                                if version_result.stdout:
                                    version_text = version_result.stdout.strip()
                                else:
                                    version_text = version_result.stderr.strip()
                                
                                if version_text.startswith("Python "):
                                    exact_version = version_text.split(" ")[1]
                                    self.python_combo.addItem(f"Python {exact_version} ({path})", path)
                            except:
                                # If error, just add with the expected version
                                self.python_combo.addItem(f"{version} ({path})", path)
                    except:
                        pass
        except:
            # If anything fails, at least we have the system Python option
            pass
        
        # Add option to create a new environment
        self.python_combo.addItem("Create New Environment", "new")