from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLabel, QPushButton, QLineEdit, QComboBox, QCheckBox,
                               QGroupBox, QSpinBox, QFileDialog)
from PySide6.QtCore import Qt

from gui.utils.styles import BUTTON_STYLE, CARD_STYLE

class SettingsView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Create settings sections
        self._create_general_settings()
        self._create_network_settings()
        self._create_mining_settings()
        
        # Save button
        self.save_button = QPushButton("Save Settings")
        self.save_button.setStyleSheet(BUTTON_STYLE)
        self.save_button.clicked.connect(self.save_settings)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        
        self.layout.addLayout(button_layout)
        self.layout.addStretch()
    
    def _create_general_settings(self):
        # General settings group
        general_group = QGroupBox("General Settings")
        general_group.setStyleSheet(CARD_STYLE)
        
        form_layout = QFormLayout(general_group)
        form_layout.setContentsMargins(16, 16, 16, 16)
        form_layout.setSpacing(12)
        
        # Settings fields
        self.gpu_select = QComboBox()
        self.gpu_select.addItems(["All GPUs", "GPU 0", "GPU 1", "CPU Only"])
        
        self.startup_check = QCheckBox("Launch on system startup")
        self.notifications_check = QCheckBox("Enable notifications")
        self.update_check = QCheckBox("Check for updates automatically")
        
        # Add to form layout
        form_layout.addRow("GPU Selection:", self.gpu_select)
        form_layout.addRow("", self.startup_check)
        form_layout.addRow("", self.notifications_check)
        form_layout.addRow("", self.update_check)
        
        self.layout.addWidget(general_group)
    
    def _create_network_settings(self):
        # Network settings group
        network_group = QGroupBox("Network Settings")
        network_group.setStyleSheet(CARD_STYLE)
        
        form_layout = QFormLayout(network_group)
        form_layout.setContentsMargins(16, 16, 16, 16)
        form_layout.setSpacing(12)
        
        # Settings fields
        self.network_select = QComboBox()
        self.network_select.addItems(["Commune", "Bittensor", "Both"])
        
        self.wallet_path = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self._browse_wallet)
        
        wallet_layout = QHBoxLayout()
        wallet_layout.addWidget(self.wallet_path)
        wallet_layout.addWidget(self.browse_button)
        
        self.node_endpoint = QLineEdit()
        self.node_endpoint.setPlaceholderText("Optional custom node endpoint")
        
        # Add to form layout
        form_layout.addRow("Default Network:", self.network_select)
        form_layout.addRow("Wallet File:", wallet_layout)
        form_layout.addRow("Node Endpoint:", self.node_endpoint)
        
        self.layout.addWidget(network_group)
    
    def _create_mining_settings(self):
        # Mining settings group
        mining_group = QGroupBox("Mining Settings")
        mining_group.setStyleSheet(CARD_STYLE)
        
        form_layout = QFormLayout(mining_group)
        form_layout.setContentsMargins(16, 16, 16, 16)
        form_layout.setSpacing(12)
        
        # Settings fields
        self.threads = QSpinBox()
        self.threads.setRange(1, 64)
        self.threads.setValue(4)
        
        self.memory_limit = QSpinBox()
        self.memory_limit.setRange(1, 64)
        self.memory_limit.setValue(8)
        self.memory_limit.setSuffix(" GB")
        
        self.auto_restart = QCheckBox("Automatically restart on errors")
        
        # Add to form layout
        form_layout.addRow("Mining Threads:", self.threads)
        form_layout.addRow("Memory Limit:", self.memory_limit)
        form_layout.addRow("", self.auto_restart)
        
        self.layout.addWidget(mining_group)
    
    def _browse_wallet(self):
        """Open file dialog to select wallet file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Wallet File", "", "Wallet Files (*.json *.wallet);;All Files (*)"
        )
        if file_path:
            self.wallet_path.setText(file_path)
    
    def save_settings(self):
        """Save the settings"""
        # In a real implementation, this would save to a config file
        print("Settings saved")