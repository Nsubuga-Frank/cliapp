# gui/components/mining_console.py
from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
                               QLabel, QPushButton, QTextEdit, QTabWidget)
from PySide6.QtCore import Qt

class MiningConsole(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polaris Miner Node")
        self.setMinimumSize(640, 480)  # Reduced window size
        
        # Central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)  # Reduced margins
        
        # Add tabs
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Dashboard tab
        dashboard_tab = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_tab)
        dashboard_layout.setSpacing(10)  # Reduced spacing
        
        # Create header
        header = QLabel("Polaris Miner Node")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        header.setAlignment(Qt.AlignCenter)
        dashboard_layout.addWidget(header)
        
        # Node status
        self.status_label = QLabel("Node Status: Ready to Start")
        self.status_label.setStyleSheet("font-size: 14px; color: #5F6368;")
        self.status_label.setAlignment(Qt.AlignCenter)
        dashboard_layout.addWidget(self.status_label)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 5, 0, 10)  # Reduced margins
        
        # Start mining button
        self.start_button = QPushButton("Start Mining")
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4285F4;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 12px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1A73E8;
            }
        """)
        self.start_button.clicked.connect(self.start_mining)
        
        # Stop mining button
        self.stop_button = QPushButton("Stop Mining")
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #EA4335;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px 12px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #D93025;
            }
            QPushButton:disabled {
                background-color: #E8EAED;
                color: #9AA0A6;
            }
        """)
        self.stop_button.clicked.connect(self.stop_mining)
        self.stop_button.setEnabled(False)
        
        # Add buttons to layout
        button_layout.addStretch()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addStretch()
        
        dashboard_layout.addLayout(button_layout)
        
        # Mining log label
        log_label = QLabel("Mining Log")
        log_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 5px;")
        dashboard_layout.addWidget(log_label)
        
        # Console output
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("""
            background-color: #1e1e1e;
            color: #f0f0f0;
            font-family: monospace;
            font-size: 12px;
            border-radius: 4px;
            padding: 8px;
        """)
        dashboard_layout.addWidget(self.console)
        
        # Add tab to tab widget
        self.tabs.addTab(dashboard_tab, "Dashboard")
        
        # Settings tab
        settings_tab = QWidget()
        self.tabs.addTab(settings_tab, "Settings")
        
        # Initial messages
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