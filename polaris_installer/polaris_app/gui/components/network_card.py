from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt

class NetworkCard(QWidget):
    def __init__(self, title, description, is_available=True, color="gray", parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: white;
            border: 1px solid #E8EAED;
            border-radius: 6px;
            padding: 8px;
        """)
        self.setFixedHeight(110)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        header = QHBoxLayout()
        dot = QLabel()
        dot.setFixedSize(10, 10)
        dot.setStyleSheet(f"background-color: {self._color_code(color)}; border-radius: 5px;")
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold; font-size: 11px;")
        status_label = QLabel("Available" if is_available else "Coming Soon")
        status_label.setStyleSheet("""
            background-color: #34A853 if is_available else #FBBC05;
            color: white if is_available else black;
            font-size: 9px;
            padding: 2px 4px;
            border-radius: 3px;
        """)

        header.addWidget(dot)
        header.addWidget(title_label)
        header.addStretch()
        header.addWidget(status_label)
        layout.addLayout(header)

        desc_label = QLabel(description)
        desc_label.setStyleSheet("font-size: 10px; color: #5F6368;")
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)

    def _color_code(self, color):
        return {
            "blue": "#4285F4",
            "yellow": "#FBBC05",
            "green": "#34A853",
            "red": "#EA4335",
            "gray": "#5F6368"
        }.get(color, "#5F6368")
