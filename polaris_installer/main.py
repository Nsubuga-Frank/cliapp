# main.py
import os
import sys

from src.installer import PolarisInstaller


def main():
    # Ensure we're in the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Create and run the installer application
    app = PolarisInstaller()
    app.run()

if __name__ == "__main__":
    main()