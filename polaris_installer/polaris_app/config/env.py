import os

INSTALL_DIR = os.path.expanduser("~/Polaris")
VENV_PYTHON = os.path.join(INSTALL_DIR, "venv", "bin", "python")
VENV_PIP = os.path.join(INSTALL_DIR, "venv", "bin", "pip")
VENV_BIN = os.path.join(INSTALL_DIR, "venv", "bin")

if os.name == "nt":
    VENV_PYTHON = os.path.join(INSTALL_DIR, "venv", "Scripts", "python.exe")
    VENV_PIP = os.path.join(INSTALL_DIR, "venv", "Scripts", "pip.exe")
    VENV_BIN = os.path.join(INSTALL_DIR, "venv", "Scripts")
