import os
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QGroupBox, QScrollArea, QSizePolicy, QPushButton, QMessageBox, QProgressBar
)
from PySide6.QtCore import Qt, QRegularExpression, QTimer, QThread, Signal
from PySide6.QtGui import QRegularExpressionValidator, QColor

from gui.utils.bittensor_utils import (
    start_bittensor_miner, stop_bittensor_miner, 
    is_bittensor_running, get_uid_from_hotkey, 
    BITTENSOR_AVAILABLE
)

class MinerThread(QThread):
    """Thread for executing miner operations without blocking the UI"""
    result_signal = Signal(dict)
    
    def __init__(self, operation, params=None):
        super().__init__()
        self.operation = operation
        self.params = params or {}
        
    def run(self):
        result = {"success": False, "message": "Operation failed"}
        
        try:
            if self.operation == "start_miner":
                wallet_name = self.params.get("wallet_name")
                hotkey = self.params.get("hotkey", "default")
                netuid = self.params.get("netuid", 49)
                network = self.params.get("network", "finney")
                
                success, message = start_bittensor_miner(wallet_name, hotkey, netuid, network)
                result = {"success": success, "message": message}
                
            elif self.operation == "stop_miner":
                success, message = stop_bittensor_miner()
                result = {"success": success, "message": message}
                
            elif self.operation == "check_miner_status":
                is_running = is_bittensor_running()
                result = {"success": True, "is_running": is_running}
                
        except Exception as e:
            result = {"success": False, "message": f"Operation error: {str(e)}"}
        
        self.result_signal.emit(result)

class SubnetStep(QWidget):
    def __init__(self):
        super().__init__()
        self.data = {}

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 5, 20, 20)  # Reduced top margin from 20 to 5

        # Scrollable area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setSpacing(10)
        scroll_layout.setContentsMargins(0, 0, 0, 0)  # No internal margins

        # Form
        form_group = QGroupBox("📋 Enter Subnet Info")
        form_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                margin-top: 5px;  /* Reduced from 10px */
                padding-top: 5px;  /* Reduced from 10px */
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        form_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        form_layout = QVBoxLayout(form_group)
        form_layout.setSpacing(6)  # Reduced from 8
        form_layout.setContentsMargins(15, 15, 15, 15)  # Reduced top from 20 to 15

        input_style = """
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: white;
                min-width: 150px;
            }
            QLineEdit:focus {
                border: 1px solid #1a73e8;
            }
            QLabel {
                font-weight: normal;
                padding-left: 2px;
            }
        """

        name_validator = QRegularExpressionValidator(QRegularExpression("^[a-zA-Z0-9_]+$"))
        numeric_validator = QRegularExpressionValidator(QRegularExpression("^[0-9]+$"))

        # Create wallet details in one row
        wallet_row = QHBoxLayout()
        wallet_row.setSpacing(15)
        
        # Coldkey column
        coldkey_col = QVBoxLayout()
        coldkey_col.setSpacing(4)
        coldkey_col.addWidget(QLabel("Coldkey Name:"))
        self.coldkey_input = QLineEdit()
        self.coldkey_input.setPlaceholderText("e.g., mywallet")
        self.coldkey_input.setStyleSheet(input_style)
        self.coldkey_input.setValidator(name_validator)
        self.coldkey_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        coldkey_col.addWidget(self.coldkey_input)
        wallet_row.addLayout(coldkey_col)
        
        # Hotkey column
        hotkey_col = QVBoxLayout()
        hotkey_col.setSpacing(4)
        hotkey_col.addWidget(QLabel("Hotkey Name:"))
        self.hotkey_input = QLineEdit()
        self.hotkey_input.setPlaceholderText("e.g., default")
        self.hotkey_input.setStyleSheet(input_style)
        self.hotkey_input.setValidator(name_validator)
        self.hotkey_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        hotkey_col.addWidget(self.hotkey_input)
        wallet_row.addLayout(hotkey_col)
        
        # Add the wallet row to the form
        form_layout.addLayout(wallet_row)
        
        # Add warning message
        warning_label = QLabel("⚠️ Warning: The wallet details provided must match the wallet used to register on the subnet.")
        warning_label.setStyleSheet("color: #d32f2f; font-weight: bold; padding: 5px;")
        warning_label.setWordWrap(True)
        form_layout.addWidget(warning_label)
        
        # Other fields
        self.uid_input = QLineEdit()
        self.uid_input.setPlaceholderText("e.g., 49")
        self.uid_input.setStyleSheet(input_style)
        self.uid_input.setValidator(numeric_validator)
        self.uid_input.setText("49")  # Set default to mainnet
        self.uid_input.setReadOnly(True)
        self.uid_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.miner_uid_input = QLineEdit()
        self.miner_uid_input.setPlaceholderText("e.g., 123")
        self.miner_uid_input.setStyleSheet(input_style)
        self.miner_uid_input.setValidator(numeric_validator)
        self.miner_uid_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add remaining fields to form
        form_layout.addWidget(QLabel("Subnet UID:"))
        form_layout.addWidget(self.uid_input)
        form_layout.addWidget(QLabel("Miner UID:"))
        form_layout.addWidget(self.miner_uid_input)
        form_layout.addStretch(1)  # Add stretch at the bottom

        scroll_layout.addWidget(form_group)
        scroll_layout.addStretch(1)  # Add stretch at the bottom

        # Add verify button
        self.verify_button = QPushButton("Verify Registration")
        self.verify_button.clicked.connect(self.verify_registration)
        form_layout.addWidget(self.verify_button)
        
        # Add verification status
        self.verify_status = QLabel("")
        self.verify_status.setWordWrap(True)
        form_layout.addWidget(self.verify_status)
        
        # Create miner control group
        miner_group = QGroupBox("Miner Control")
        miner_layout = QVBoxLayout(miner_group)
        miner_layout.setContentsMargins(15, 20, 15, 15)
        miner_layout.setSpacing(10)
        
        # Miner status
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status:"))
        self.status_label = QLabel("Checking...")
        self.status_label.setStyleSheet("font-weight: bold;")
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()
        miner_layout.addLayout(status_layout)
        
        # Miner control buttons
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("Start Miner")
        self.start_button.clicked.connect(self.start_miner)
        self.start_button.setEnabled(False)
        
        self.stop_button = QPushButton("Stop Miner")
        self.stop_button.clicked.connect(self.stop_miner)
        self.stop_button.setEnabled(False)
        
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        miner_layout.addLayout(button_layout)
        
        # Add the miner group to the scroll layout
        scroll_layout.addWidget(miner_group)
        
        # Add stretch at the bottom
        scroll_layout.addStretch(1)

        # Default values
        self.hotkey_input.setText("default")

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # Set size policies and minimum size for the widget
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(500, 400)

        # Create timer to check miner status
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.check_miner_status)
        self.status_timer.start(5000)  # Check every 5 seconds
        
        # Initial status check
        self.check_miner_status()

    def verify_registration(self):
        """Verify that the wallet is registered on the subnet"""
        coldkey = self.coldkey_input.text().strip()
        hotkey = self.hotkey_input.text().strip()
        netuid = self.uid_input.text().strip()
        
        if not coldkey or not hotkey:
            QMessageBox.warning(self, "Verification Error", "Please enter both coldkey and hotkey names.")
            return
            
        self.verify_status.setText("Verifying registration... Please wait.")
        self.verify_status.setStyleSheet("color: #666;")
        
        # Create and start the thread
        self.thread = MinerThread("check_miner_status")
        self.thread.result_signal.connect(self.handle_verification_result)
        self.thread.start()
        
    def handle_verification_result(self, result):
        """Handle verification result"""
        if not BITTENSOR_AVAILABLE:
            self.verify_status.setText("Bittensor not installed. Please install it first.")
            self.verify_status.setStyleSheet("color: red;")
            return
            
        # Get the hotkey's UID
        success, data = get_uid_from_hotkey(
            self.hotkey_input.text().strip(), 
            int(self.uid_input.text().strip()),
            "finney"
        )
        
        if success:
            uid = data.get("uid")
            self.miner_uid_input.setText(str(uid))
            self.verify_status.setText(f"Registration verified! Miner UID: {uid}")
            self.verify_status.setStyleSheet("color: green; font-weight: bold;")
            self.start_button.setEnabled(True)
        else:
            self.verify_status.setText(f"Verification failed: {data.get('error', 'Hotkey not registered on subnet')}")
            self.verify_status.setStyleSheet("color: red;")
            self.start_button.setEnabled(False)
    
    def check_miner_status(self):
        """Check if the miner is running"""
        self.thread = MinerThread("check_miner_status")
        self.thread.result_signal.connect(self.update_miner_status)
        self.thread.start()
    
    def update_miner_status(self, result):
        """Update the miner status display"""
        if result["success"]:
            is_running = result.get("is_running", False)
            if is_running:
                self.status_label.setText("Running")
                self.status_label.setStyleSheet("font-weight: bold; color: green;")
                self.start_button.setEnabled(False)
                self.stop_button.setEnabled(True)
            else:
                self.status_label.setText("Stopped")
                self.status_label.setStyleSheet("font-weight: bold; color: red;")
                # Only enable start if we have a valid UID
                if self.miner_uid_input.text().strip():
                    self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
        else:
            self.status_label.setText("Unknown")
            self.status_label.setStyleSheet("font-weight: bold; color: orange;")
    
    def start_miner(self):
        """Start the miner"""
        coldkey = self.coldkey_input.text().strip()
        hotkey = self.hotkey_input.text().strip()
        netuid = self.uid_input.text().strip()
        
        if not coldkey or not hotkey or not netuid:
            QMessageBox.warning(self, "Start Error", "Please fill in all required fields.")
            return
            
        # Confirm start
        reply = QMessageBox.question(
            self,
            "Confirm Start",
            f"Start mining with wallet '{coldkey}' and hotkey '{hotkey}' on subnet {netuid}?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Disable buttons during operation
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.status_label.setText("Starting...")
            
            # Start the miner in a thread
            params = {
                "wallet_name": coldkey,
                "hotkey": hotkey,
                "netuid": int(netuid),
                "network": "finney"
            }
            
            self.thread = MinerThread("start_miner", params)
            self.thread.result_signal.connect(self.handle_start_result)
            self.thread.start()
    
    def handle_start_result(self, result):
        """Handle the result of starting the miner"""
        if result["success"]:
            self.status_label.setText("Running")
            self.status_label.setStyleSheet("font-weight: bold; color: green;")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            QMessageBox.information(self, "Miner Started", "The miner has been started successfully.")
        else:
            self.status_label.setText("Error")
            self.status_label.setStyleSheet("font-weight: bold; color: red;")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            QMessageBox.critical(self, "Start Error", f"Failed to start miner: {result['message']}")
    
    def stop_miner(self):
        """Stop the miner"""
        # Confirm stop
        reply = QMessageBox.question(
            self,
            "Confirm Stop",
            "Stop the running miner?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Disable buttons during operation
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.status_label.setText("Stopping...")
            
            # Stop the miner in a thread
            self.thread = MinerThread("stop_miner")
            self.thread.result_signal.connect(self.handle_stop_result)
            self.thread.start()
    
    def handle_stop_result(self, result):
        """Handle the result of stopping the miner"""
        if result["success"]:
            self.status_label.setText("Stopped")
            self.status_label.setStyleSheet("font-weight: bold; color: red;")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            QMessageBox.information(self, "Miner Stopped", "The miner has been stopped successfully.")
        else:
            self.status_label.setText("Error")
            self.status_label.setStyleSheet("font-weight: bold; color: orange;")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            QMessageBox.critical(self, "Stop Error", f"Failed to stop miner: {result['message']}")

    def get_data(self):
        return {
            "coldkey": self.coldkey_input.text().strip(),
            "hotkey": self.hotkey_input.text().strip(),
            "netuid": self.uid_input.text().strip(),
            "miner_uid": self.miner_uid_input.text().strip(),
            "network": "finney"  # Always mainnet
        }
