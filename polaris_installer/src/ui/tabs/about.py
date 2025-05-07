# src/ui/tabs/about.py
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout, QWidget


class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        
        # Create layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setAlignment(Qt.AlignCenter)
        
        # Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        if os.path.exists(os.path.join("resources", "images", "logo.png")):
            pixmap = QPixmap(os.path.join("resources", "images", "logo.png"))
            logo_label.setPixmap(pixmap.scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.layout.addWidget(logo_label)
        
        # Product name
        product_name = QLabel("Polaris Miner")
        product_name.setAlignment(Qt.AlignCenter)
        product_name.setStyleSheet("font-weight: bold; font-size: 16px; margin-top: 10px;")
        self.layout.addWidget(product_name)
        
        # Version
        version = QLabel("Version 1.0.2")
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet("color: #4B5563; font-size: 12px;")
        self.layout.addWidget(version)
        
        # Description
        description = QLabel("Polaris is a mining node for the Bittensor network, allowing you to contribute computing resources to earn rewards.")
        description.setAlignment(Qt.AlignCenter)
        description.setWordWrap(True)
        description.setStyleSheet("font-size: 12px; margin-top: 10px; max-width: 400px;")
        self.layout.addWidget(description)
        
        # Copyright
        copyright = QLabel("© 2025 Polaris Network. All rights reserved.")
        copyright.setAlignment(Qt.AlignCenter)
        copyright.setStyleSheet("font-size: 12px; margin-top: 5px;")
        self.layout.addWidget(copyright)
        
        # Contact info frame
        info_frame = QFrame()
        info_frame.setStyleSheet("""
            background-color: #F9FAFB;
            border: 1px solid #E5E7EB;
            border-radius: 4px;
            padding: 10px;
            margin-top: 15px;
            max-width: 400px;
        """)
        info_layout = QVBoxLayout(info_frame)
        
        # Website
        website_layout = QHBoxLayout()
        website_label = QLabel("Website:")
        website_label.setStyleSheet("color: #4B5563; font-size: 12px;")
        website_value = QLabel("https://polariscloud.ai")
        website_value.setStyleSheet("color: #2563EB; font-size: 12px;")
        website_layout.addWidget(website_label)
        website_layout.addStretch()
        website_layout.addWidget(website_value)
        info_layout.addLayout(website_layout)
        
        # Support
        support_layout = QHBoxLayout()
        support_label = QLabel("Support:")
        support_label.setStyleSheet("color: #4B5563; font-size: 12px;")
        support_value = QLabel("support@polariscloud.ai")
        support_value.setStyleSheet("color: #2563EB; font-size: 12px;")
        support_layout.addWidget(support_label)
        support_layout.addStretch()
        support_layout.addWidget(support_value)
        info_layout.addLayout(support_layout)
        
        self.layout.addWidget(info_frame, alignment=Qt.AlignCenter)