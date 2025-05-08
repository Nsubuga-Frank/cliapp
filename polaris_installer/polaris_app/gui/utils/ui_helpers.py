from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtCore import Qt
from gui.utils.styles import BLACK, BLUE, GRAY, FONT_SMALL, FONT_MEDIUM, FONT_LARGE

def create_heading(text, size=20, color=BLACK, alignment=Qt.AlignLeft):
    """Create a heading label with the specified text, size, and color"""
    label = QLabel(text)
    label.setStyleSheet(f"font-size: {size}px; font-weight: bold; color: {color};")
    label.setAlignment(alignment)
    return label

def create_subheading(text, size=22, color=BLUE, alignment=Qt.AlignLeft):
    """Create a subheading label with the specified text, size, and color"""
    label = QLabel(text)
    label.setStyleSheet(f"font-size: {size}px; font-weight: bold; color: {color};")
    label.setAlignment(alignment)
    return label

def create_description(text, size=12, color=GRAY, alignment=Qt.AlignLeft, word_wrap=True):
    """Create a description label with the specified text, size, and color"""
    label = QLabel(text)
    label.setStyleSheet(f"font-size: {size}px; color: {color}; margin-top: 5px;")
    label.setAlignment(alignment)
    label.setWordWrap(word_wrap)
    return label

def create_spacer(fixed_width=None, fixed_height=None):
    """Create a spacer with the specified width and height"""
    spacer = QLabel()
    
    if fixed_width:
        spacer.setFixedWidth(fixed_width)
    else:
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
    if fixed_height:
        spacer.setFixedHeight(fixed_height)
    else:
        spacer.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        
    return spacer