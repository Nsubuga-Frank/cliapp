# src/config/settings.py
"""
Configuration settings for Polaris Installer
"""

# Default installation settings
DEFAULT_SETTINGS = {
    "install_dir": "~/Polaris",
    "create_shortcut": True,
    "add_to_path": True,
    "launch_on_startup": False,
    "use_system_python": True,
}

# Package requirements
REQUIRED_PACKAGES = [
    "pyside6==6.5.2",
    "bittensor-cli",
    "numpy==1.24.3"
]

# Application metadata
APP_METADATA = {
    "name": "Polaris Miner",
    "version": "1.0.2",
    "description": "A mining node for the Bittensor network",
    "company": "Polaris Network",
    "website": "https://polariscloud.ai",
    "support": "support@polariscloud.ai"
}

# UI theme settings
UI_THEME = {
    "primary_color": "#2563EB",
    "secondary_color": "#1F2937",
    "background_color": "#FFFFFF",
    "text_color": "#4B5563",
    "accent_color": "#3B82F6"
}