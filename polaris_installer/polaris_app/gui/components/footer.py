# gui/components/footer.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

class FooterComponent(QWidget):
    def __init__(self, company_name, version):
        super().__init__()
        
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 5, 0, 5)  # Reduced margins
        
        # Company name
        company = QLabel(company_name)
        company.setStyleSheet("color: #5F6368; font-size: 12px;")
        
        # Version
        version_label = QLabel(version)
        version_label.setStyleSheet("color: #5F6368; font-size: 12px;")
        
        # Add to footer layout
        layout.addWidget(company)
        layout.addStretch()
        layout.addWidget(version_label)