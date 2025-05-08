import os
import sys
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QGroupBox, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator, QColor


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

        # Default values
        self.hotkey_input.setText("default")

        scroll_area.setWidget(scroll_widget)
        main_layout.addWidget(scroll_area)

        # Set size policies and minimum size for the widget
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(500, 400)

    def get_data(self):
        return {
            "coldkey": self.coldkey_input.text().strip(),
            "hotkey": self.hotkey_input.text().strip(),
            "netuid": self.uid_input.text().strip(),
            "miner_uid": self.miner_uid_input.text().strip(),
            "network": "finney"  # Always mainnet
        }
