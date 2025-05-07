# src/ui/tabs/general.py
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget


class GeneralTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with icon and title
        header_layout = QHBoxLayout()
        
        # Icon
        icon_label = QLabel()
        if os.path.exists(os.path.join("resources", "images", "logo.png")):
            pixmap = QPixmap(os.path.join("resources", "images", "logo.png"))
            icon_label.setPixmap(pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        header_layout.addWidget(icon_label)
        
        # Title and description
        title_layout = QVBoxLayout()
        title = QLabel("Polaris Miner Installer")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        description = QLabel("Setup utility for Polaris mining node")
        description.setStyleSheet("color: #4B5563; font-size: 12px;")
        
        title_layout.addWidget(title)
        title_layout.addWidget(description)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()
        
        self.layout.addLayout(header_layout)
        
        # Version information
        info_layout = QVBoxLayout()
        
        # Version
        version_layout = QHBoxLayout()
        version_label = QLabel("Version:")
        version_label.setStyleSheet("color: #4B5563; font-size: 12px; min-width: 80px;")
        version_value = QLabel("1.0.2")
        version_value.setStyleSheet("font-size: 12px;")
        version_layout.addWidget(version_label)
        version_layout.addWidget(version_value)
        version_layout.addStretch()
        info_layout.addLayout(version_layout)
        
        # Network
        network_layout = QHBoxLayout()
        network_label = QLabel("Network:")
        network_label.setStyleSheet("color: #4B5563; font-size: 12px; min-width: 80px;")
        network_value = QLabel("Bittensor")
        network_value.setStyleSheet("font-size: 12px;")
        network_layout.addWidget(network_label)
        network_layout.addWidget(network_value)
        network_layout.addStretch()
        info_layout.addLayout(network_layout)
        
        # Subnet
        subnet_layout = QHBoxLayout()
        subnet_label = QLabel("Subnet:")
        subnet_label.setStyleSheet("color: #4B5563; font-size: 12px; min-width: 80px;")
        subnet_value = QLabel("PolarisCloud.ai (19)")
        subnet_value.setStyleSheet("font-size: 12px;")
        subnet_layout.addWidget(subnet_label)
        subnet_layout.addWidget(subnet_value)
        subnet_layout.addStretch()
        info_layout.addLayout(subnet_layout)
        
        self.layout.addLayout(info_layout)
        
        # Ensure the layout expands properly
        self.layout.addStretch()