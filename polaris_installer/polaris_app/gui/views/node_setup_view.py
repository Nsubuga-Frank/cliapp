from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget,
    QProgressBar, QGroupBox, QFormLayout, QRadioButton, QButtonGroup,
    QLineEdit, QGridLayout
)
from PySide6.QtCore import Qt
from gui.utils.system_info import get_full_system_info


class NodeSetupView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        title = QLabel("Polaris Node Setup")
        title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        nav_layout = QHBoxLayout()
        self.register_button = QPushButton("Register Miner")
        self.register_button.clicked.connect(self.show_register_panel)
        self.register_button.setStyleSheet(self._button_style(True))

        self.advanced_button = QPushButton("Advanced Options")
        self.advanced_button.clicked.connect(self.show_advanced_panel)
        self.advanced_button.setStyleSheet(self._button_style(False))

        nav_layout.addWidget(self.register_button)
        nav_layout.addWidget(self.advanced_button)
        nav_layout.addStretch()
        layout.addLayout(nav_layout)

        self.content_stack = QStackedWidget()
        layout.addWidget(self.content_stack)

        self.content_stack.addWidget(self._create_register_panel())
        self.content_stack.addWidget(self._create_advanced_panel())
        self.content_stack.setCurrentIndex(0)

    def _button_style(self, selected):
        return """
            QPushButton {{
                background-color: {bg};
                color: {fg};
                border-radius: 4px;
                padding: 6px 14px;
                font-size: 11px;
                font-weight: {weight};
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
        """.format(
            bg="#4285F4" if selected else "#F1F3F4",
            fg="white" if selected else "#333",
            weight="bold" if selected else "normal",
            hover="#1A73E8" if selected else "#E8EAED"
        )

    def show_register_panel(self):
        self.content_stack.setCurrentIndex(0)
        self.register_button.setStyleSheet(self._button_style(True))
        self.advanced_button.setStyleSheet(self._button_style(False))

    def show_advanced_panel(self):
        self.content_stack.setCurrentIndex(1)
        self.register_button.setStyleSheet(self._button_style(False))
        self.advanced_button.setStyleSheet(self._button_style(True))

    def _create_register_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        title = QLabel("Miner Setup Steps")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(20)  # Adjusted for 5 steps
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(5)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                background-color: #E0E0E0;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #42A5F5, stop:1 #5C6BC0);
                border-radius: 3px;
            }
        """)
        layout.addWidget(self.progress_bar)

        step_nav = QHBoxLayout()
        self.steps = [
            ("System Info", "🖥️"),
            ("Network", "🌐"),
            ("Wallet", "💳"),
            ("Subnet", "🛡️"),
            ("Register", "✅")
        ]
        self.step_labels = []

        for i, (name, icon) in enumerate(self.steps):
            label = QLabel(f"<div align='center' style='font-size:10px;'>{icon}<br>{name}</div>")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: #34A853; font-weight: bold;" if i == 0 else "color: #999;")
            self.step_labels.append(label)
            step_nav.addWidget(label)

        layout.addLayout(step_nav)

        self.step_stack = QStackedWidget()
        layout.addWidget(self.step_stack)

        for index, (name, _) in enumerate(self.steps):
            step_widget = QWidget()
            step_layout = QVBoxLayout(step_widget)

            if index == 0:  # System Info
                # Auto-detected system info
                auto_system_info = get_full_system_info()[0]
                self.collected_system_info = auto_system_info  # Save initial info
                
                # Create box for system info
                auto_info_box = QGroupBox("Detected System Info")
                auto_info_box.setStyleSheet("""
                    QGroupBox {
                        font-weight: bold;
                        border: 1px solid #E0E0E0;
                        border-radius: 6px;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 5px;
                    }
                    QLabel {
                        padding: 4px 0;
                    }
                """)
                
                # Create a grid layout for the two-column display
                auto_grid = QGridLayout()
                auto_grid.setHorizontalSpacing(20)
                auto_grid.setVerticalSpacing(6)
                
                # System info - Left column
                left_labels = [
                    ("Hostname:", auto_system_info["hostname"]),
                    ("OS:", auto_system_info["operating_system"]),
                    ("Public IP:", auto_system_info["public_ip"]),
                    ("Internal IP:", auto_system_info["ip_address"]),
                    ("RAM:", auto_system_info["compute_resources"][0]["ram"])
                ]
                
                # System info - Right column
                cpu = auto_system_info["compute_resources"][0]["cpu_specs"]
                right_labels = [
                    ("CPU Model:", cpu["model"]),
                    ("Cores:", str(cpu["cores"])),
                    ("Threads:", str(cpu["threads"])),
                    ("Frequency:", cpu["frequency"])
                ]
                
                # Add items to the grid
                for i, (label_text, value) in enumerate(left_labels):
                    label = QLabel(label_text)
                    label.setStyleSheet("font-weight: bold; color: #555;")
                    value_label = QLabel(value)
                    value_label.setStyleSheet("color: #333;")
                    auto_grid.addWidget(label, i, 0)
                    auto_grid.addWidget(value_label, i, 1)
                
                for i, (label_text, value) in enumerate(right_labels):
                    label = QLabel(label_text)
                    label.setStyleSheet("font-weight: bold; color: #555;")
                    value_label = QLabel(value)
                    value_label.setStyleSheet("color: #333;")
                    auto_grid.addWidget(label, i, 2)
                    auto_grid.addWidget(value_label, i, 3)
                
                # Set column stretch to ensure proper alignment
                auto_grid.setColumnStretch(1, 1)
                auto_grid.setColumnStretch(3, 1)
                
                auto_info_box.setLayout(auto_grid)
                step_layout.addWidget(auto_info_box)
                
                # Create box for user input
                user_info_box = QGroupBox("Network Connection Details")
                user_info_box.setStyleSheet("""
                    QGroupBox {
                        font-weight: bold;
                        border: 1px solid #1A73E8;
                        border-radius: 6px;
                        margin-top: 10px;
                        background-color: #F5F9FF;
                    }
                    QGroupBox::title {
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 5px;
                    }
                """)
                user_form = QFormLayout()
                
                # Username field
                self.username_input = QLineEdit()
                self.username_input.setText(auto_system_info["compute_resources"][0]["network"]["username"])
                self.username_input.setPlaceholderText("Enter system username")
                self.username_input.setStyleSheet("""
                    padding: 6px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                """)
                user_form.addRow("Username:", self.username_input)
                
                # Port fields in one row
                ports_widget = QWidget()
                ports_layout = QHBoxLayout(ports_widget)
                ports_layout.setContentsMargins(0, 0, 0, 0)
                
                self.port1_input = QLineEdit()
                self.port1_input.setPlaceholderText("e.g., 22")
                if auto_system_info["compute_resources"][0]["network"]["open_ports"]:
                    self.port1_input.setText(auto_system_info["compute_resources"][0]["network"]["open_ports"][0])
                else:
                    self.port1_input.setText("22")
                    
                self.port2_input = QLineEdit()
                self.port2_input.setPlaceholderText("e.g., 8080")
                if len(auto_system_info["compute_resources"][0]["network"]["open_ports"]) > 1:
                    self.port2_input.setText(auto_system_info["compute_resources"][0]["network"]["open_ports"][1])
                else:
                    self.port2_input.setText("8080")
                
                # Style for port inputs
                port_style = """
                    padding: 6px;
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    min-width: 80px;
                    max-width: 100px;
                """
                self.port1_input.setStyleSheet(port_style)
                self.port2_input.setStyleSheet(port_style)
                
                ports_layout.addWidget(self.port1_input)
                ports_layout.addWidget(QLabel("and"))
                ports_layout.addWidget(self.port2_input)
                ports_layout.addStretch()
                
                user_form.addRow("Open Ports:", ports_widget)
                
                # Connection preview
                self.conn_preview = QLabel()
                self.update_connection_preview()
                self.conn_preview.setStyleSheet("font-family: monospace; color: #1A73E8;")
                
                # Connect signals to update preview
                self.username_input.textChanged.connect(self.update_connection_preview)
                self.port1_input.textChanged.connect(self.update_connection_preview)
                
                user_form.addRow("SSH Connection:", self.conn_preview)
                
                user_info_box.setLayout(user_form)
                step_layout.addWidget(user_info_box)

            elif index == 1:  # Network Selection
                self.selected_network = None
                group = QGroupBox("Select a Network")
                group.setStyleSheet("QGroupBox { font-weight: bold; }")
                vbox = QVBoxLayout()

                self.network_buttons = QButtonGroup()

                # Active: Bittensor
                btn_bittensor = QRadioButton("🌐  Bittensor Network")
                btn_bittensor.setStyleSheet("""
                    QRadioButton {
                        font-size: 12px;
                        padding: 8px;
                        border: 1px solid #4285F4;
                        border-radius: 6px;
                        background-color: #E8F0FE;
                    }
                    QRadioButton::indicator { width: 0px; height: 0px; }
                    QRadioButton:hover { background-color: #D2E3FC; }
                """)
                btn_bittensor.clicked.connect(lambda: self._set_network("Bittensor"))
                vbox.addWidget(btn_bittensor)
                self.network_buttons.addButton(btn_bittensor)

                def disabled_radio(name):
                    rb = QRadioButton(f"🔒  {name} (Coming Soon)")
                    rb.setEnabled(False)
                    rb.setStyleSheet("""
                        QRadioButton {
                            font-size: 12px;
                            padding: 8px;
                            color: #999;
                            border: 1px solid #E0E0E0;
                            border-radius: 6px;
                            background-color: #F5F5F5;
                        }
                    """)
                    return rb

                vbox.addWidget(disabled_radio("Commune Network"))
                vbox.addWidget(disabled_radio("Polaris Network"))

                group.setLayout(vbox)
                step_layout.addWidget(group)
            elif index == 2:
              from gui.steps.wallet_step import WalletStep
              step_layout.addWidget(WalletStep())
              
            elif index == 3:
              from gui.steps.subnet_step import SubnetStep
              step_layout.addWidget(SubnetStep())

            else:
                msg = QLabel(f"{name} step content goes here...")
                msg.setStyleSheet("font-size: 11px; color: #555;")
                step_layout.addWidget(msg)

            step_layout.addStretch()
            self.step_stack.addWidget(step_widget)

        btn_layout = QHBoxLayout()

        self.prev_btn = QPushButton("Previous")
        self.prev_btn.setFixedSize(80, 28)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #E0E0E0;
                color: #333;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #DADCE0;
            }
        """)
        self.prev_btn.clicked.connect(self._prev_step)
        self.prev_btn.setEnabled(False)

        self.next_btn = QPushButton("Next")
        self.next_btn.setFixedSize(80, 28)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #4285F4;
                color: white;
                border-radius: 4px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1A73E8;
            }
        """)
        self.next_btn.clicked.connect(self._next_step)

        btn_layout.addWidget(self.prev_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.next_btn)
        layout.addLayout(btn_layout)

        self.current_step = 0
        return panel
        
    def update_connection_preview(self):
        """Updates the SSH connection preview label based on current inputs"""
        username = self.username_input.text().strip() or "username"
        port = self.port1_input.text().strip() or "22"
        ip = self.collected_system_info["public_ip"]
        self.conn_preview.setText(f"ssh://{username}@{ip}:{port}")

    def _set_network(self, name):
        self.selected_network = name

    def _next_step(self):
        if self.current_step < len(self.steps) - 1:
            # If leaving the system info step, update with user input
            if self.current_step == 0:
                username = self.username_input.text().strip()
                ports = [self.port1_input.text().strip(), self.port2_input.text().strip()]
                # Update collected system info with user inputs
                updated_info = get_full_system_info(username=username, open_ports=ports)[0]
                self.collected_system_info = updated_info
            
            self.current_step += 1
            self.step_stack.setCurrentIndex(self.current_step)
            self.progress_bar.setValue(int((self.current_step + 1) / len(self.steps) * 100))
            self._update_step_styles()
            self.prev_btn.setEnabled(self.current_step > 0)
            self.next_btn.setText("Next" if self.current_step < len(self.steps) - 1 else "Finish")

    def _prev_step(self):
        if self.current_step > 0:
            self.current_step -= 1
            self.step_stack.setCurrentIndex(self.current_step)
            self.progress_bar.setValue(int((self.current_step + 1) / len(self.steps) * 100))
            self._update_step_styles()
            self.prev_btn.setEnabled(self.current_step > 0)
            self.next_btn.setText("Next" if self.current_step < len(self.steps) - 1 else "Finish")

    def _update_step_styles(self):
        for i, label in enumerate(self.step_labels):
            if i == self.current_step:
                label.setStyleSheet("color: #34A853; font-weight: bold;")
            else:
                label.setStyleSheet("color: #999;")

    def _create_advanced_panel(self):
        import json
        from PySide6.QtWidgets import QTextEdit

        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)

        title = QLabel("System Information (Advanced View)")
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title)

        self.specs_box = QTextEdit()
        self.specs_box.setReadOnly(True)
        self.specs_box.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #E8EAED;
            border-radius: 4px;
            padding: 10px;
            font-size: 11px;
            line-height: 1.4;
        """)
        
        # Initial system info
        initial_info = get_full_system_info()
        self.specs_box.setPlainText(json.dumps(initial_info, indent=2))
        layout.addWidget(self.specs_box)

        # Add a refresh button
        refresh_btn = QPushButton("Refresh System Info")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #4285F4;
                color: white;
                border-radius: 4px;
                padding: 6px 14px;
                font-size: 11px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1A73E8;
            }
        """)
        refresh_btn.clicked.connect(self._refresh_system_info)
        layout.addWidget(refresh_btn)

        layout.addStretch()
        return panel
        
    def _refresh_system_info(self):
        """Refreshes the advanced view with latest system info including user inputs"""
        import json
        
        # Get the latest input values if available
        if hasattr(self, 'username_input') and hasattr(self, 'port1_input') and hasattr(self, 'port2_input'):
            username = self.username_input.text().strip()
            ports = [self.port1_input.text().strip(), self.port2_input.text().strip()]
            info = get_full_system_info(username=username, open_ports=ports)
        else:
            info = get_full_system_info()
            
        self.specs_box.setPlainText(json.dumps(info, indent=2))
