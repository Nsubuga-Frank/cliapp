from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton

def create_action_buttons(start_callback):
    section = QWidget()
    layout = QHBoxLayout(section)
    layout.setContentsMargins(0, 10, 0, 5)
    layout.setSpacing(10)

    start_btn = QPushButton("Get Started")
    start_btn.setFixedSize(100, 28)
    start_btn.setStyleSheet("""
        QPushButton {
            background-color: #4285F4;
            color: white;
            border-radius: 3px;
            font-size: 11px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #1A73E8;
        }
    """)
    start_btn.clicked.connect(start_callback)

    learn_btn = QPushButton("Learn More")
    learn_btn.setFixedSize(100, 28)
    learn_btn.setStyleSheet("""
        QPushButton {
            background-color: white;
            color: #333;
            border: 1px solid #E8EAED;
            border-radius: 3px;
            font-size: 11px;
        }
        QPushButton:hover {
            background-color: #F1F3F4;
        }
    """)

    layout.addWidget(start_btn)
    layout.addWidget(learn_btn)
    layout.addStretch()

    return section
