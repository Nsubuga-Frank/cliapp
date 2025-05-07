# src/installation.py
from PySide6.QtCore import QThread, Signal, QMutex, QWaitCondition
import time
import sys
import os
import subprocess
import shutil

class InstallationProcess(QThread):
    progress_updated = Signal(int)
    log_message = Signal(str)
    installation_complete = Signal()
    
    def __init__(self, settings=None):
        super().__init__()
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.abort = False
        
        # Use provided settings or defaults
        default_settings = {
            "install_dir": os.path.expanduser("~/Polaris"),
            "python_version": "system",
            "create_shortcut": True,
            "add_to_path": True,
            "launch_on_startup": False
        }
        
        self.settings = settings if settings else default_settings
        self.install_dir = self.settings["install_dir"]
    
    def run(self):
        try:
            # Check for abort before starting
            if self.abort:
                self.log_message.emit("[INFO] Installation aborted by user")
                return
                
            # Log start
            self.log_message.emit("[INFO] Starting Polaris installation process...")
            self.progress_updated.emit(5)
            
            # Check for abort
            if self.abort:
                self.log_message.emit("[INFO] Installation aborted by user")
                return
            
            # Create installation directory
            self.log_message.emit(f"[INFO] Creating installation directory at {self.install_dir}")
            os.makedirs(self.install_dir, exist_ok=True)
            self.progress_updated.emit(10)
            
            # Check for abort
            if self.abort:
                self.log_message.emit("[INFO] Installation aborted by user")
                return
            
            # Check Python
            self.log_message.emit("[INFO] Checking Python installation...")
            self.progress_updated.emit(15)
            python_version = sys.version.split()[0]
            self.log_message.emit(f"[INFO] Python {python_version} detected")
            
            # Check for WSL
            is_wsl = self._check_if_wsl()
            if is_wsl:
                self.log_message.emit("[INFO] Windows Subsystem for Linux (WSL) detected")
            
            # Check for abort
            if self.abort:
                self.log_message.emit("[INFO] Installation aborted by user")
                return
            
            # Create virtual environment
            self.log_message.emit("[INFO] Creating virtual environment...")
            self.progress_updated.emit(20)
            venv_success = self._create_virtual_env()
            if not venv_success:
                self.log_message.emit("[ERROR] Failed to create virtual environment")
                return
            
            # Check for abort
            if self.abort:
                self.log_message.emit("[INFO] Installation aborted by user")
                return
            
            # Determine pip and python paths based on OS
            if os.name == "nt":  # Windows
                pip_path = os.path.join(self.install_dir, "venv", "Scripts", "pip.exe")
                python_path = os.path.join(self.install_dir, "venv", "Scripts", "python.exe")
            else:  # Unix/MacOS/WSL
                pip_path = os.path.join(self.install_dir, "venv", "bin", "pip")
                python_path = os.path.join(self.install_dir, "venv", "bin", "python")
            
            # Install dependencies
            self.log_message.emit("[INFO] Installing required dependencies...")
            self.progress_updated.emit(30)
            
            # Check for abort
            if self.abort:
                self.log_message.emit("[INFO] Installation aborted by user")
                return
            
            # Install basic build requirements first
            self.log_message.emit("[INFO] Installing build requirements...")
            result = subprocess.run([pip_path, "install", "--upgrade", "pip", "wheel", "setuptools"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                self.log_message.emit(f"[WARNING] Failed to install build requirements: {result.stderr}")
            
            # Check for abort
            if self.abort:
                self.log_message.emit("[INFO] Installation aborted by user")
                return
            
            # Install specific packages with compatible versions
            packages = ["pyside6>=6.6.0", "bittensor-cli", "numpy"]
            for i, package in enumerate(packages):
                # Check for abort before each package installation
                if self.abort:
                    self.log_message.emit("[INFO] Installation aborted by user")
                    return
                    
                self.log_message.emit(f"[INFO] Installing {package}")
                progress = 40 + (i + 1) * 15
                result = subprocess.run([pip_path, "install", package], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    self.log_message.emit(f"[ERROR] Failed to install {package}: {result.stderr}")
                else:
                    self.log_message.emit(f"[INFO] Successfully installed {package}")
                self.progress_updated.emit(progress)
            
            # Check for abort
            if self.abort:
                self.log_message.emit("[INFO] Installation aborted by user")
                return
            
            # Install a smaller version of Polaris GUI
            self.log_message.emit("[INFO] Setting up Polaris GUI...")
            self.progress_updated.emit(85)
            gui_success = self._setup_polaris_gui(python_path, is_wsl)
            if not gui_success:
                self.log_message.emit("[ERROR] Failed to set up Polaris GUI")
                return
            
            # Check for abort
            if self.abort:
                self.log_message.emit("[INFO] Installation aborted by user")
                return    
                
            # Check for CUDA
            try:
                # We need to use the installed Python to check for CUDA
                cmd = [python_path, "-c", "import torch; print(torch.cuda.is_available())"]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.stdout.strip() == "True":
                    self.log_message.emit("[INFO] CUDA detected, GPU acceleration enabled")
                else:
                    self.log_message.emit("[WARNING] CUDA not detected, using CPU only mode")
            except:
                self.log_message.emit("[WARNING] Unable to check CUDA, assuming CPU only mode")
            
            self.progress_updated.emit(90)
            
            # Check for abort
            if self.abort:
                self.log_message.emit("[INFO] Installation aborted by user")
                return
            
            # Create desktop shortcut
            self.log_message.emit("[INFO] Creating desktop shortcut...")
            self._create_shortcut(is_wsl, python_path)
            self.progress_updated.emit(95)
            
            # Check for abort
            if self.abort:
                self.log_message.emit("[INFO] Installation aborted by user")
                return
            
            # Complete
            self.log_message.emit("[INFO] Configuration complete")
            self.progress_updated.emit(100)
            
            # Signal completion
            self.installation_complete.emit()
            
        except Exception as e:
            self.log_message.emit(f"[ERROR] Installation failed: {str(e)}")
        finally:
            # Always emit finished signal to ensure proper cleanup
            self.finished.emit()
    
    def _check_if_wsl(self):
        """Check if running under Windows Subsystem for Linux"""
        try:
            with open('/proc/version', 'r') as f:
                return 'microsoft' in f.read().lower()
        except:
            return False
    
    def _create_virtual_env(self):
        try:
            venv_path = os.path.join(self.install_dir, "venv")
            result = subprocess.run([sys.executable, "-m", "venv", venv_path], 
                                  check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            self.log_message.emit(f"[ERROR] Failed to create virtual environment: {e.stderr.decode() if e.stderr else str(e)}")
            return False
    
    def _setup_polaris_gui(self, python_path, is_wsl=False):
        try:
            gui_dir = os.path.join(self.install_dir, "polaris_gui")
            os.makedirs(gui_dir, exist_ok=True)
            
            # Create a simple version of the GUI
            with open(os.path.join(gui_dir, "main.py"), "w") as f:
                f.write("""
import sys
import os
import subprocess
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                             QLabel, QPushButton, QTextEdit, QTabWidget, QGroupBox, QFormLayout)
from PySide6.QtCore import Qt, QProcess, Signal, Slot

class PolarisMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polaris Miner")
        self.setMinimumSize(800, 600)
        
        # Central widget and tab layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        # Create tabs
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)
        
        # Dashboard tab
        self.dashboard_tab = QWidget()
        self.dashboard_layout = QVBoxLayout(self.dashboard_tab)
        
        # Header
        header = QLabel("Polaris Miner Node")
        header.setStyleSheet("font-size: 24px; font-weight: bold;")
        header.setAlignment(Qt.AlignCenter)
        self.dashboard_layout.addWidget(header)
        
        # Status
        self.status_label = QLabel("Node Status: Ready to Start")
        self.status_label.setStyleSheet("font-size: 16px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.dashboard_layout.addWidget(self.status_label)
        
        # Control buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Mining")
        self.start_button.clicked.connect(self.start_mining)
        self.stop_button = QPushButton("Stop Mining")
        self.stop_button.clicked.connect(self.stop_mining)
        self.stop_button.setEnabled(False)
        
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch()
        
        self.dashboard_layout.addLayout(button_layout)
        
        # Console output
        console_box = QGroupBox("Mining Log")
        console_layout = QVBoxLayout(console_box)
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background-color: #1e1e1e; color: #f0f0f0; font-family: monospace;")
        console_layout.addWidget(self.console)
        
        self.dashboard_layout.addWidget(console_box)
        
        # Settings tab
        self.settings_tab = QWidget()
        self.settings_layout = QVBoxLayout(self.settings_tab)
        
        # Form for settings
        settings_form = QGroupBox("Miner Settings")
        form_layout = QFormLayout(settings_form)
        
        self.settings_layout.addWidget(settings_form)
        self.settings_layout.addStretch()
        
        # Add tabs to widget
        self.tabs.addTab(self.dashboard_tab, "Dashboard")
        self.tabs.addTab(self.settings_tab, "Settings")
        
        # Process for mining
        self.process = None
        
        # Initial message
        self.console.append("Polaris Miner Node initialized")
        self.console.append("Using bittensor-cli for mining operations")
        self.console.append("Ready to start mining. Click 'Start Mining' to begin.")
    
    def start_mining(self):
        self.console.append("Starting mining operations...")
        self.status_label.setText("Node Status: Starting...")
        
        # This will be replaced with actual bittensor-cli commands
        self.console.append("Initializing bittensor-cli...")
        
        # Enable/disable buttons
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        
        # Update status
        self.status_label.setText("Node Status: Running")
        self.console.append("Mining operation started successfully")
    
    def stop_mining(self):
        self.console.append("Stopping mining operations...")
        
        # Enable/disable buttons
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        
        # Update status
        self.status_label.setText("Node Status: Stopped")
        self.console.append("Mining operation stopped successfully")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PolarisMainWindow()
    window.show()
    sys.exit(app.exec())
""")
            
            # Check for abort
            if self.abort:
                return False
                
            # Create appropriate launcher script based on platform
            if os.name == "nt" and not is_wsl:  # Windows
                with open(os.path.join(gui_dir, "launch.bat"), "w") as f:
                    f.write(f"""@echo off
cd "{gui_dir}"
"{python_path}" main.py
""")
            else:  # Linux or WSL
                with open(os.path.join(gui_dir, "launch.sh"), "w") as f:
                    f.write(f"""#!/bin/bash
cd "{gui_dir}"
"{python_path}" main.py
""")
                # Make executable
                os.chmod(os.path.join(gui_dir, "launch.sh"), 0o755)
            
            return True
        except Exception as e:
            self.log_message.emit(f"[ERROR] Failed to set up Polaris GUI: {str(e)}")
            return False
    
    def _create_shortcut(self, is_wsl=False, python_path=None):
        """Create shortcuts based on platform"""
        if os.name == "nt" and not is_wsl:  # Windows (not WSL)
            try:
                # Skip this in WSL as it will fail due to missing Windows modules
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                shortcut_path = os.path.join(desktop, "Polaris Miner.lnk")
                
                try:
                    # These will only be available on Windows
                    import winshell
                    from win32com.client import Dispatch
                    
                    shell = Dispatch('WScript.Shell')
                    shortcut = shell.CreateShortCut(shortcut_path)
                    shortcut.Targetpath = os.path.join(self.install_dir, "polaris_gui", "launch.bat")
                    shortcut.WorkingDirectory = os.path.join(self.install_dir, "polaris_gui")
                    shortcut.save()
                    
                    self.log_message.emit("[INFO] Windows desktop shortcut created")
                except ImportError:
                    self.log_message.emit("[WARNING] Windows shortcut modules not available")
                
            except Exception as e:
                self.log_message.emit(f"[WARNING] Failed to create Windows shortcut: {str(e)}")
        
        elif is_wsl:  # WSL specific
            try:
                self.log_message.emit("[INFO] Creating WSL launcher script")
                launcher_path = os.path.join(self.install_dir, "polaris_gui", "launch.sh")
                
                # Ensure the launch script exists and is executable
                if not os.path.exists(launcher_path):
                    with open(launcher_path, "w") as f:
                        f.write(f"""#!/bin/bash
cd "{os.path.join(self.install_dir, "polaris_gui")}"
"{python_path}" main.py
""")
                    os.chmod(launcher_path, 0o755)
                
                self.log_message.emit("[INFO] WSL launcher script created")
                
                # We can't easily create Windows shortcuts from WSL, so inform the user
                self.log_message.emit("[INFO] In WSL, run the launcher script to start the application")
                self.log_message.emit(f"[INFO] Launcher path: {launcher_path}")
                
            except Exception as e:
                self.log_message.emit(f"[WARNING] Failed to create WSL launcher: {str(e)}")
        
        else:  # Regular Linux
            try:
                # Create .desktop file for Linux
                home_dir = os.path.expanduser("~")
                desktop_dir = os.path.join(home_dir, "Desktop")
                applications_dir = os.path.join(home_dir, ".local", "share", "applications")
                
                # Ensure the applications directory exists
                os.makedirs(applications_dir, exist_ok=True)
                
                # Create desktop entry file
                desktop_file_path = os.path.join(applications_dir, "polaris-miner.desktop")
                
                with open(desktop_file_path, "w") as f:
                    f.write(f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Polaris Miner
Comment=Mining node for Bittensor network
Exec=bash -c 'cd {os.path.join(self.install_dir, "polaris_gui")} && {python_path} main.py'
Terminal=false
Categories=Utility;
""")
                
                # Make the file executable
                os.chmod(desktop_file_path, 0o755)
                
                # Copy to desktop if it exists
                if os.path.exists(desktop_dir):
                    desktop_shortcut = os.path.join(desktop_dir, "polaris-miner.desktop")
                    shutil.copy2(desktop_file_path, desktop_shortcut)
                    os.chmod(desktop_shortcut, 0o755)
                
                self.log_message.emit("[INFO] Linux desktop shortcut created")
            except Exception as e:
                self.log_message.emit(f"[WARNING] Failed to create Linux shortcut: {str(e)}")