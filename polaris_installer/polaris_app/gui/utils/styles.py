# Polaris Miner Node styles
from PySide6.QtGui import QColor

# Colors
BLUE = "#4285F4"
LIGHT_BLUE = "#8AB4F8"
DARK_BLUE = "#1A73E8"
YELLOW = "#FBBC05"
GREEN = "#34A853"
RED = "#EA4335"
WHITE = "#FFFFFF"
BLACK = "#202124"
GRAY = "#5F6368"
LIGHT_GRAY = "#E8EAED"
BACKGROUND = "#F8F9FA"

# Font sizes - reduced
FONT_LARGE = 18  # reduced from 24
FONT_MEDIUM = 13  # reduced from 16
FONT_SMALL = 10  # reduced from 12

# Style sheets
HEADER_STYLE = f'''
    color: {BLUE};
    font-size: {FONT_LARGE}px;
    font-weight: bold;
    margin-bottom: 6px;
'''

SUBHEADER_STYLE = f'''
    color: {BLACK};
    font-size: {FONT_MEDIUM}px;
    font-weight: bold;
'''

BUTTON_STYLE = f'''
    QPushButton {{
        background-color: {BLUE};
        color: {WHITE};
        border: none;
        border-radius: 3px;
        padding: 5px 10px;
        font-weight: bold;
        font-size: {FONT_SMALL}px;
    }}
    QPushButton:hover {{
        background-color: {DARK_BLUE};
    }}
    QPushButton:disabled {{
        background-color: {LIGHT_GRAY};
        color: {GRAY};
    }}
'''

SECONDARY_BUTTON_STYLE = f'''
    QPushButton {{
        background-color: {WHITE};
        color: {BLACK};
        border: 1px solid {LIGHT_GRAY};
        border-radius: 3px;
        padding: 5px 10px;
        font-size: {FONT_SMALL}px;
    }}
    QPushButton:hover {{
        background-color: {LIGHT_GRAY};
    }}
'''

CONSOLE_STYLE = f'''
    background-color: {BLACK};
    color: {WHITE};
    font-family: monospace;
    font-size: {FONT_SMALL}px;
    border-radius: 3px;
    padding: 6px;
'''

CARD_STYLE = f'''
    background-color: {WHITE};
    border: 1px solid {LIGHT_GRAY};
    border-radius: 5px;
    padding: 10px;
'''

AVAILABLE_BADGE = f'''
    background-color: {GREEN};
    color: {WHITE};
    border-radius: 3px;
    padding: 2px 5px;
    font-weight: bold;
    font-size: {FONT_SMALL}px;
'''

COMING_SOON_BADGE = f'''
    background-color: {YELLOW};
    color: {BLACK};
    border-radius: 3px;
    padding: 2px 5px;
    font-weight: bold;
    font-size: {FONT_SMALL}px;
'''

# New compact style for smaller UIs
COMPACT_STYLE = f'''
    QLabel, QCheckBox, QRadioButton, QComboBox, QSpinBox, QLineEdit, QTextEdit {{
        font-size: {FONT_SMALL}px;
    }}
    QPushButton {{
        font-size: {FONT_SMALL}px;
        padding: 3px 6px;
    }}
    QGroupBox {{
        font-size: {FONT_SMALL}px;
        padding-top: 14px;
        margin-top: 8px;
    }}
'''