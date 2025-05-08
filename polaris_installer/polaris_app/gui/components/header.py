from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from gui.utils.styles import BLUE, WHITE, LIGHT_GRAY

class HeaderComponent(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setFixedHeight(60)
        self.setStyleSheet(f"background-color: {WHITE}; border-bottom: 1px solid {LIGHT_GRAY};")
        
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # Logo (placeholder)
        logo_label = QLabel()
        logo_label.setFixedSize(32, 32)
        
        # Try to load a logo if available
        logo_path = "../resources/images/logo.png"
        logo_pixmap = QPixmap(logo_path)
        if not logo_pixmap.isNull():
            logo_label.setPixmap(logo_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            # Fallback to text
            logo_label.setText("🖥️")
            logo_label.setStyleSheet("font-size: 24px;")
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {BLUE}; font-size: 18px; font-weight: bold; padding-left: 10px;")
        
        # Add widgets to layout
        layout.addWidget(logo_label)
        layout.addWidget(title_label)
        layout.addStretch()