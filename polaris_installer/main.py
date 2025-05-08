# main.py
import os
import sys

# Force Qt to use X11 backend instead of Wayland
os.environ["QT_QPA_PLATFORM"] = "xcb"

from src.installer import PolarisInstaller


def main():
    # Ensure we're in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create and run the installer application
    app = PolarisInstaller()
    app.run()

if __name__ == "__main__":
    main()