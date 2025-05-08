from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTextBrowser)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap

from gui.utils.styles import BLUE, BLACK, GRAY, WHITE, CARD_STYLE

class AboutView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Logo and app info
        self._create_app_info()
        
        # Description
        self._create_description()
        
        # Version info
        self._create_version_info()
        
        # Add stretch to push everything to the top
        self.layout.addStretch()
    
    def _create_app_info(self):
        # App info section
        info_widget = QWidget()
        info_widget.setStyleSheet(CARD_STYLE)
        info_layout = QVBoxLayout(info_widget)
        
        # Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        
        # Try to load a logo if available
        logo_path = "../../resources/images/logo.png"
        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(QSize(120, 120), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # Fallback to text
            logo_label.setText("🖥️")
            logo_label.setStyleSheet("font-size: 72px; text-align: center;")
        
        # App name
        app_name = QLabel("Polaris Miner Node")
        app_name.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {BLUE};")
        app_name.setAlignment(Qt.AlignCenter)
        
        # Company
        company = QLabel("PolarisCloud")
        company.setStyleSheet(f"font-size: 14px; color: {GRAY};")
        company.setAlignment(Qt.AlignCenter)
        
        # Add to layout
        info_layout.addWidget(logo_label)
        info_layout.addWidget(app_name)
        info_layout.addWidget(company)
        
        self.layout.addWidget(info_widget)
    
    def _create_description(self):
        # Description section
        desc_widget = QWidget()
        desc_widget.setStyleSheet(CARD_STYLE)
        desc_layout = QVBoxLayout(desc_widget)
        
        # About title
        about_title = QLabel("About")
        about_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {BLACK};")
        
        # Description text
        desc_text = QTextBrowser()
        desc_text.setOpenExternalLinks(True)
        desc_text.setStyleSheet("border: none; background: transparent;")
        desc_text.setHtml("""
        <p>Polaris Miner Node is a decentralized compute mining application that allows you to connect your GPU to various blockchain networks and earn rewards.</p>
        
        <p>Connect with worldwide compute providers to access CPU, GPU, and AI resources through our distributed network.</p>
        
        <p>For more information, visit <a href="https://polariscloud.io">https://polariscloud.io</a></p>
        """)
        
        # Add to layout
        desc_layout.addWidget(about_title)
        desc_layout.addWidget(desc_text)
        
        self.layout.addWidget(desc_widget)
    
    def _create_version_info(self):
        # Version info section
        version_widget = QWidget()
        version_widget.setStyleSheet(CARD_STYLE)
        version_layout = QVBoxLayout(version_widget)
        
        # Version title
        version_title = QLabel("Version Information")
        version_title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {BLACK};")
        
        # Version details
        version_text = QTextBrowser()
        version_text.setOpenExternalLinks(False)
        version_text.setStyleSheet("border: none; background: transparent;")
        version_text.setHtml("""
        <p><b>Application Version:</b> 1.0.0</p>
        <p><b>Build Date:</b> May 7, 2025</p>
        <p><b>Python Version:</b> 3.10.4</p>
        <p><b>PySide6 Version:</b> 6.6.0</p>
        <p><b>Bittensor CLI Version:</b> 1.2.3</p>
        """)
        
        # Add to layout
        version_layout.addWidget(version_title)
        version_layout.addWidget(version_text)
        
        self.layout.addWidget(version_widget)