from PySide6.QtWidgets import QTextEdit

class TerminalConsole(QTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setStyleSheet("""
            background-color: #1e1e1e;
            color: #d4d4d4;
            font-family: Consolas, monospace;
            font-size: 11px;
            border: 1px solid #3c3c3c;
            border-radius: 4px;
            padding: 6px;
        """)

    def log(self, message):
        self.append(f"> {message}")
