import os
import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QScrollArea, QSizePolicy

class WalletStep(QWidget):
    def __init__(self):
        super().__init__()
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 5, 20, 20)
        
        # Scrollable area for instructions
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QScrollArea.NoFrame)
        scroll_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Instructions text
        instructions = QTextEdit()
        instructions.setReadOnly(True)
        instructions.setHtml("""
            <h3 style="color: #333; margin-top: 0;">📡 Subnet Registration</h3>
            <p>Before continuing, register your hotkey using the following command:</p>

            <div style="background-color: #f5f5f5; padding: 10px; border-left: 3px solid #1a73e8; margin: 10px 0;">
                <b>🌐 Mainnet</b><br>
                <code>btcli subnets register --wallet-name mywallet --hotkey default --netuid 49 --network finney</code>
            </div>

            <p>Once complete, proceed to the next step to enter your subnet details.</p>
            
            <h4 style="color: #333; margin-top: 20px;">Additional Information</h4>
            <p>When registering on a subnet:</p>
            <ul>
                <li>Make sure your wallet has enough TAO for the registration transaction</li>
                <li>The registration process may take a few minutes to complete</li>
                <li>You can verify your registration using: <code>btcli wallet overview</code></li>
            </ul>
        """)
        
        instructions.setStyleSheet("""
            background-color: #f9f9f9;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 10px;
            min-width: 500px;
        """)
        instructions.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Create a container widget for the QTextEdit
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.addWidget(instructions)
        
        # Add container to scroll area
        scroll_area.setWidget(container)
        
        # Add scrollable area to main layout
        layout.addWidget(scroll_area)
        
        # Set size policies and minimum size for the widget
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(500, 400)
