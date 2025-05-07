# src/ui/tabs/installer.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                              QPushButton, QProgressBar, QTextEdit, QFrame)
from PySide6.QtCore import Qt, QTimer, Signal, Slot
from PySide6.QtGui import QColor, QTextCursor

import os
import subprocess
import sys

from src.installation import InstallationProcess

class InstallerTab(QWidget):
    # Signal to request starting installation
    start_installation_requested = Signal(dict)
    
    def __init__(self):
        super().__init__()
        
        # Create the installation process handler
        self.installation = None
        
        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Status section
        self.status_label = QLabel("Installation Status")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.layout.addWidget(self.status_label)
        
        # Status message
        self.status_frame = QFrame()
        self.status_frame.setStyleSheet("""
            background-color: #EFF6FF; 
            border: 1px solid #BFDBFE; 
            border-radius: 4px;
        """)
        self.status_frame_layout = QVBoxLayout(self.status_frame)
        
        self.status_message = QLabel("Ready to install Polaris Miner. Click Install to continue.")
        self.status_message.setStyleSheet("color: #1E40AF; font-size: 12px;")
        self.status_frame_layout.addWidget(self.status_message)
        
        self.layout.addWidget(self.status_frame)
        
        # Button section
        self.button_layout = QHBoxLayout()
        self.install_button = QPushButton("Install")
        self.install_button.setStyleSheet("""
            background-color: #2563EB; 
            color: white; 
            padding: 6px 16px; 
            border-radius: 4px;
            font-size: 12px;
        """)
        self.install_button.clicked.connect(self.request_installation)
        
        self.button_layout.addWidget(self.install_button)
        self.button_layout.addStretch()
        self.layout.addLayout(self.button_layout)
        
        # Progress bar - initially hidden
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #E5E7EB;
                border-radius: 2px;
                background-color: #F3F4F6;
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #2563EB;
                border-radius: 2px;
            }
        """)
        self.layout.addWidget(self.progress_bar)
        
        # Logs section
        self.logs_label = QLabel("Installation Logs")
        self.logs_label.setStyleSheet("font-weight: bold; font-size: 12px; margin-top: 10px;")
        self.layout.addWidget(self.logs_label)
        
        self.logs_text = QTextEdit()
        self.logs_text.setReadOnly(True)
        self.logs_text.setStyleSheet("""
            background-color: #1F2937; 
            color: #D1D5DB; 
            border-radius: 4px;
            font-family: monospace;
            font-size: 10px;
        """)
        self.logs_text.setText("Installation logs will appear here when you start the installation process.")
        self.layout.addWidget(self.logs_text)
        
        # Ensure the layout expands properly
        self.layout.addStretch()
        
        # Installation settings
        self.installation_settings = {}
    
    def update_settings(self, settings):
        """Update installation settings"""
        self.installation_settings = settings
    
    def request_installation(self):
        """Request to start installation with current settings"""
        self.start_installation_requested.emit(self.installation_settings)
        self.start_installation(self.installation_settings)
    
    def start_installation(self, settings=None):
        """Start the installation process"""
        if settings:
            self.installation_settings = settings
        
        # Clean up any existing installation thread
        self.cleanup_installation()
        
        # Update UI for installation in progress
        self.install_button.setEnabled(False)
        self.install_button.setText("Installing...")
        self.install_button.setStyleSheet("""
            background-color: #9CA3AF; 
            color: white; 
            padding: 6px 16px; 
            border-radius: 4px;
            font-size: 12px;
        """)
        
        # Show progress bar
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Clear logs
        self.logs_text.clear()
        
        # Update status message
        self.status_message.setText("Installing Polaris components...")
        self.status_frame.setStyleSheet("""
            background-color: #F0F9FF; 
            border: 1px solid #BAE6FD; 
            border-radius: 4px;
        """)
        
        # Create and connect installation process
        self.installation = InstallationProcess(self.installation_settings)
        self.installation.progress_updated.connect(self.update_progress)
        self.installation.log_message.connect(self.add_log_message)
        self.installation.installation_complete.connect(self.installation_completed)
        self.installation.finished.connect(self.installation_finished)
        
        # Start the installation process
        self.installation.start()
    
    @Slot(int)
    def update_progress(self, value):
        """Update the progress bar"""
        self.progress_bar.setValue(value)
    
    @Slot(str)
    def add_log_message(self, message):
        """Add a message to the log display"""
        self.logs_text.append(message)
        # Auto-scroll to bottom
        cursor = self.logs_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.logs_text.setTextCursor(cursor)
    
    @Slot()
    def installation_completed(self):
        """Handle installation completion"""
        self.status_message.setText("Installation completed successfully!")
        self.status_frame.setStyleSheet("""
            background-color: #ECFDF5; 
            border: 1px solid #A7F3D0; 
            border-radius: 4px;
        """)
        
        # Update Launch button
        self.install_button.setText("Launch Polaris")
        self.install_button.setEnabled(True)
        self.install_button.setStyleSheet("""
            background-color: #2563EB; 
            color: white; 
            padding: 6px 16px; 
            border-radius: 4px;
            font-size: 12px;
        """)
        
        # Disconnect previous connections and connect to launch method
        try:
            self.install_button.clicked.disconnect()
        except:
            pass
        self.install_button.clicked.connect(self.launch_application)
    
    @Slot()
    def installation_finished(self):
        """Handle installation thread finished (whether successful or not)"""
        # This gets called when the thread finishes, regardless of completion status
        # Make sure the thread is cleaned up properly
        if self.installation and not self.installation.isRunning():
            self.installation = None
    
    def cleanup_installation(self):
        """Clean up installation thread if it exists"""
        if hasattr(self, 'installation') and self.installation:
            if self.installation.isRunning():
                # Tell the thread to abort
                self.installation.abort = True
                # Wait with timeout
                if not self.installation.wait(1000):  # 1 second timeout
                    self.installation.terminate()
                    self.installation.wait()
            self.installation = None
    
    def launch_application(self):
        """Launch the installed Polaris application"""
        try:
            # Get the path to the launcher script
            if hasattr(self, 'installation') and hasattr(self.installation, 'install_dir'):
                install_dir = self.installation.install_dir
            else:
                # Default path if install_dir is not available
                install_dir = os.path.expanduser("~/Polaris")
            
            # Determine the launcher path based on platform
            if os.name == "nt":  # Windows
                launcher_path = os.path.join(install_dir, "polaris_gui", "launch.bat")
            else:  # Linux/macOS/WSL
                launcher_path = os.path.join(install_dir, "polaris_gui", "launch.sh")
            
            # Make sure the launcher exists
            if os.path.exists(launcher_path):
                self.add_log_message(f"[INFO] Launching Polaris application...")
                self.add_log_message(f"[INFO] Using launcher script: {launcher_path}")
                
                # Run in a new process so it doesn't block the installer
                if os.name == "nt":  # Windows
                    # For Windows, use the start command to run in a new window
                    subprocess.Popen(f'start cmd /c "{launcher_path}"', 
                                   shell=True, 
                                   cwd=os.path.dirname(launcher_path))
                else:  # Linux/macOS/WSL
                    # For Linux/macOS, ensure script is executable and run it
                    os.chmod(launcher_path, 0o755)  # Ensure it's executable
                    
                    # Different approach for WSL
                    is_wsl = False
                    try:
                        with open('/proc/version', 'r') as f:
                            is_wsl = 'microsoft' in f.read().lower()
                    except:
                        pass
                    
                    if is_wsl:
                        # In WSL, we need a special approach 
                        proc = subprocess.Popen(["bash", launcher_path], 
                                       shell=False,
                                       cwd=os.path.dirname(launcher_path),
                                       start_new_session=True)
                        self.add_log_message(f"[INFO] Launched using WSL bash (PID: {proc.pid})")
                    else:
                        # Regular Linux/macOS
                        proc = subprocess.Popen([launcher_path], 
                                       shell=False,
                                       cwd=os.path.dirname(launcher_path),
                                       start_new_session=True)
                        self.add_log_message(f"[INFO] Launched with PID: {proc.pid}")
                
                self.add_log_message("[INFO] Polaris application launched successfully")
            else:
                self.add_log_message(f"[ERROR] Launcher script not found at {launcher_path}")
                self.add_log_message(f"[INFO] Looking for alternate launcher script...")
                
                # Try to find any launcher script in the directory
                gui_dir = os.path.join(install_dir, "polaris_gui")
                if os.path.exists(gui_dir):
                    for file in os.listdir(gui_dir):
                        if file.startswith("launch"):
                            alt_launcher = os.path.join(gui_dir, file)
                            self.add_log_message(f"[INFO] Found alternate launcher: {alt_launcher}")
                            
                            # Try to run the alternate launcher
                            if os.name != "nt":  # Make executable on Unix
                                os.chmod(alt_launcher, 0o755)
                            
                            if file.endswith(".bat"):
                                subprocess.Popen(f'start cmd /c "{alt_launcher}"', 
                                               shell=True, 
                                               cwd=gui_dir)
                            else:
                                proc = subprocess.Popen(["bash", alt_launcher], 
                                               shell=False,
                                               cwd=gui_dir,
                                               start_new_session=True)
                            
                            self.add_log_message("[INFO] Attempted to launch using alternate script")
                            return
                
                self.add_log_message("[ERROR] No launcher scripts found. Manual launch required.")
                self.add_log_message(f"[INFO] Try running: cd {os.path.join(install_dir, 'polaris_gui')} && python main.py")
        except Exception as e:
            self.add_log_message(f"[ERROR] Failed to launch application: {str(e)}")
            # Show traceback for debugging
            import traceback
            self.add_log_message(f"[DEBUG] {traceback.format_exc()}")
    
    def hideEvent(self, event):
        """Handle when the tab is hidden"""
        super().hideEvent(event)
        # No need to do anything special here
    
    def showEvent(self, event):
        """Handle when the tab becomes visible"""
        super().showEvent(event)
        # No need to do anything special here
    
    def __del__(self):
        """Destructor to ensure thread cleanup"""
        self.cleanup_installation()