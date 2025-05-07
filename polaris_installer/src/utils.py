# src/utils.py
"""
Utility functions for Polaris Installer
"""
import logging
import os
import platform
import subprocess
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("polaris_installer")

def get_platform_info():
    """
    Get information about the current platform
    """
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
    }

def expand_path(path):
    """
    Expand a path that might contain ~ or environment variables
    """
    return os.path.expanduser(os.path.expandvars(path))

def check_python_version(min_version=(3, 7, 0)):
    """
    Check if the current Python version meets the minimum requirement
    """
    current_version = tuple(map(int, platform.python_version_tuple()))
    return current_version >= min_version

def check_disk_space(path, required_mb=500):
    """
    Check if there's enough disk space at the given path
    """
    try:
        if platform.system() == "Windows":
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(path), None, None, ctypes.pointer(free_bytes))
            free_mb = free_bytes.value / (1024 * 1024)
        else:
            stats = os.statvfs(path)
            free_mb = (stats.f_bavail * stats.f_frsize) / (1024 * 1024)
        
        return free_mb >= required_mb, free_mb
    except Exception as e:
        logger.error(f"Error checking disk space: {e}")
        return False, 0

def run_command(command, cwd=None, shell=False):
    """
    Run a command and return the output
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=shell,
            check=True,
            capture_output=True,
            text=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
    except Exception as e:
        return False, str(e)

def create_directory(path):
    """
    Create a directory and all parent directories if they don't exist
    """
    try:
        path = expand_path(path)
        os.makedirs(path, exist_ok=True)
        return True
    except Exception as e:
        logger.error(f"Failed to create directory {path}: {e}")
        return False

def check_requirements():
    """
    Check if the system meets all requirements for installation
    """
    requirements = []
    
    # Check Python version
    python_ok = check_python_version()
    requirements.append(("Python 3.7+", python_ok))
    
    # Check disk space
    space_ok, free_mb = check_disk_space(os.path.expanduser("~"))
    requirements.append((f"Disk Space (>500MB, {free_mb:.1f}MB available)", space_ok))
    
    # Check if PIP is available
    pip_ok, _ = run_command([sys.executable, "-m", "pip", "--version"])
    requirements.append(("PIP Package Manager", pip_ok))
    
    # Check if we can create virtual environments
    venv_ok, _ = run_command([sys.executable, "-m", "venv", "--help"])
    requirements.append(("Virtual Environment Support", venv_ok))
    
    return requirements