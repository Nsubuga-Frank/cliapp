from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

def create_hero_section():
    section = QWidget()
    layout = QVBoxLayout(section)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(4)

    title = QLabel("Decentralized Access to")
    title.setStyleSheet("font-size: 14px; font-weight: bold; color: #333;")

    subtitle = QLabel("Global Compute Resources")
    subtitle.setStyleSheet("font-size: 16px; font-weight: bold; color: #4285F4;")

    desc = QLabel("Connect to a global network of compute resources powered by decentralized AI infrastructure.")
    desc.setWordWrap(True)
    desc.setStyleSheet("font-size: 10px; color: #666;")

    layout.addWidget(title)
    layout.addWidget(subtitle)
    layout.addWidget(desc)

    return section
