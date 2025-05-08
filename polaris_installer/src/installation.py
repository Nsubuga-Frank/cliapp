from PySide6.QtCore import QThread, Signal, QMutex, QWaitCondition
import time
import sys
import os
import subprocess
import shutil


class InstallationProcess(QThread):
    progress_updated = Signal(int)
    log_message = Signal(str)
    installation_complete = Signal()

    def __init__(self, settings=None):
        super().__init__()
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.abort = False

        default_settings = {
            "install_dir": os.path.expanduser("~/Polaris"),
            "python_version": "system",
            "create_shortcut": True,
            "add_to_path": True,
            "launch_on_startup": False
        }

        self.settings = settings if settings else default_settings
        self.install_dir = self.settings["install_dir"]

    def run(self):
        try:
            if self.abort:
                self.log_message.emit("[INFO] Installation aborted by user")
                return

            self.log_message.emit("[INFO] Starting Polaris installation process...")
            self.progress_updated.emit(5)

            self.log_message.emit(f"[INFO] Creating installation directory at {self.install_dir}")
            os.makedirs(self.install_dir, exist_ok=True)
            self.progress_updated.emit(10)

            self.log_message.emit("[INFO] Checking Python installation...")
            self.progress_updated.emit(15)
            python_version = sys.version.split()[0]
            self.log_message.emit(f"[INFO] Python {python_version} detected")

            is_wsl = self._check_if_wsl()
            if is_wsl:
                self.log_message.emit("[INFO] Windows Subsystem for Linux (WSL) detected")

            self.log_message.emit("[INFO] Creating virtual environment...")
            self.progress_updated.emit(20)
            venv_success = self._create_virtual_env()
            if not venv_success:
                self.log_message.emit("[ERROR] Failed to create virtual environment")
                return

            if os.name == "nt":
                pip_path = os.path.join(self.install_dir, "venv", "Scripts", "pip.exe")
                python_path = os.path.join(self.install_dir, "venv", "Scripts", "python.exe")
            else:
                pip_path = os.path.join(self.install_dir, "venv", "bin", "pip")
                python_path = os.path.join(self.install_dir, "venv", "bin", "python")

            self.log_message.emit("[INFO] Installing required dependencies...")
            self.progress_updated.emit(30)

            self.log_message.emit("[INFO] Installing build requirements...")
            result = subprocess.run([pip_path, "install", "--upgrade", "pip", "wheel", "setuptools"],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                self.log_message.emit(f"[WARNING] Failed to install build requirements: {result.stderr}")

            packages = ["pyside6>=6.6.0", "bittensor-cli", "numpy"]
            for i, package in enumerate(packages):
                self.log_message.emit(f"[INFO] Installing {package}")
                progress = 40 + (i + 1) * 15
                result = subprocess.run([pip_path, "install", package],
                                        capture_output=True, text=True)
                if result.returncode != 0:
                    self.log_message.emit(f"[ERROR] Failed to install {package}: {result.stderr}")
                else:
                    self.log_message.emit(f"[INFO] Successfully installed {package}")
                self.progress_updated.emit(progress)

            self.log_message.emit("[INFO] Setting up Polaris App...")
            self.progress_updated.emit(85)
            app_success = self._setup_polaris_app(python_path, is_wsl)
            if not app_success:
                self.log_message.emit("[ERROR] Failed to set up Polaris App")
                return

            try:
                cmd = [python_path, "-c", "import torch; print(torch.cuda.is_available())"]
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.stdout.strip() == "True":
                    self.log_message.emit("[INFO] CUDA detected, GPU acceleration enabled")
                else:
                    self.log_message.emit("[WARNING] CUDA not detected, using CPU only mode")
            except:
                self.log_message.emit("[WARNING] Unable to check CUDA, assuming CPU only mode")

            self.progress_updated.emit(90)

            self.log_message.emit("[INFO] Creating desktop shortcut...")
            self._create_shortcut(is_wsl, python_path)
            self.progress_updated.emit(95)

            self.log_message.emit("[INFO] Configuration complete")
            self.progress_updated.emit(100)

            self.log_message.emit("[INFO] Launching Polaris GUI App...")

            try:
                subprocess.Popen([python_path, os.path.join(self.install_dir, "polaris_app", "main.py")])
                self.log_message.emit("[INFO] Polaris launched successfully inside virtual environment")
            except Exception as e:
                self.log_message.emit(f"[ERROR] Failed to launch GUI: {str(e)}")

            self.installation_complete.emit()

        except Exception as e:
            self.log_message.emit(f"[ERROR] Installation failed: {str(e)}")
        finally:
            self.finished.emit()

    def _check_if_wsl(self):
        try:
            with open('/proc/version', 'r') as f:
                return 'microsoft' in f.read().lower()
        except:
            return False

    def _create_virtual_env(self):
        try:
            venv_path = os.path.join(self.install_dir, "venv")
            result = subprocess.run([sys.executable, "-m", "venv", venv_path],
                                    check=True, capture_output=True)
            return True
        except subprocess.CalledProcessError as e:
            self.log_message.emit(f"[ERROR] Failed to create virtual environment: {e.stderr.decode() if e.stderr else str(e)}")
            return False

    def _setup_polaris_app(self, python_path, is_wsl=False):
        try:
            source_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "polaris_app")
            app_dir = os.path.join(self.install_dir, "polaris_app")

            os.makedirs(app_dir, exist_ok=True)

            self.log_message.emit(f"[INFO] Copying application files from {source_dir} to {app_dir}")
            self._copy_directory(source_dir, app_dir)

            scripts_dir = os.path.join(self.install_dir, "scripts")
            os.makedirs(scripts_dir, exist_ok=True)

            if os.name == "nt" and not is_wsl:
                with open(os.path.join(scripts_dir, "launch.bat"), "w") as f:
                    f.write(f"""@echo off
cd "{app_dir}"
"{python_path}" main.py
""")
            else:
                with open(os.path.join(scripts_dir, "launch.sh"), "w") as f:
                    f.write(f"""#!/bin/bash
cd "{app_dir}"
"{python_path}" main.py
""")
                os.chmod(os.path.join(scripts_dir, "launch.sh"), 0o755)

            return True
        except Exception as e:
            self.log_message.emit(f"[ERROR] Failed to set up Polaris application: {str(e)}")
            return False

    def _copy_directory(self, source, destination):
        if not os.path.exists(destination):
            os.makedirs(destination)

        for item in os.listdir(source):
            source_item = os.path.join(source, item)
            dest_item = os.path.join(destination, item)

            if os.path.isdir(source_item):
                self._copy_directory(source_item, dest_item)
            else:
                shutil.copy2(source_item, dest_item)
                self.log_message.emit(f"[INFO] Copied {source_item} to {dest_item}")

    def _create_shortcut(self, is_wsl=False, python_path=None):
        if os.name == "nt" and not is_wsl:
            try:
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                shortcut_path = os.path.join(desktop, "Polaris Miner.lnk")

                try:
                    import winshell
                    from win32com.client import Dispatch

                    shell = Dispatch('WScript.Shell')
                    shortcut = shell.CreateShortCut(shortcut_path)
                    shortcut.Targetpath = os.path.join(self.install_dir, "scripts", "launch.bat")
                    shortcut.WorkingDirectory = os.path.dirname(os.path.join(self.install_dir, "scripts", "launch.bat"))
                    shortcut.save()

                    self.log_message.emit("[INFO] Windows desktop shortcut created")
                except ImportError:
                    self.log_message.emit("[WARNING] Windows shortcut modules not available")

            except Exception as e:
                self.log_message.emit(f"[WARNING] Failed to create Windows shortcut: {str(e)}")

        elif is_wsl:
            try:
                self.log_message.emit("[INFO] Creating WSL launcher script")
                launcher_path = os.path.join(self.install_dir, "scripts", "launch.sh")

                if not os.path.exists(launcher_path):
                    with open(launcher_path, "w") as f:
                        f.write(f"""#!/bin/bash
cd "{os.path.join(self.install_dir, "polaris_app")}"
"{python_path}" main.py
""")
                    os.chmod(launcher_path, 0o755)

                self.log_message.emit("[INFO] WSL launcher script created")
                self.log_message.emit("[INFO] In WSL, run the launcher script to start the application")
                self.log_message.emit(f"[INFO] Launcher path: {launcher_path}")

            except Exception as e:
                self.log_message.emit(f"[WARNING] Failed to create WSL launcher: {str(e)}")

        else:
            try:
                home_dir = os.path.expanduser("~")
                desktop_dir = os.path.join(home_dir, "Desktop")
                applications_dir = os.path.join(home_dir, ".local", "share", "applications")

                os.makedirs(applications_dir, exist_ok=True)

                desktop_file_path = os.path.join(applications_dir, "polaris-miner.desktop")

                with open(desktop_file_path, "w") as f:
                    f.write(f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Polaris Miner
Comment=Mining node for Bittensor network
Exec=bash -c 'cd {os.path.join(self.install_dir, "polaris_app")} && {python_path} main.py'
Terminal=false
Categories=Utility;
""")

                os.chmod(desktop_file_path, 0o755)

                if os.path.exists(desktop_dir):
                    desktop_shortcut = os.path.join(desktop_dir, "polaris-miner.desktop")
                    shutil.copy2(desktop_file_path, desktop_shortcut)
                    os.chmod(desktop_shortcut, 0o755)

                self.log_message.emit("[INFO] Linux desktop shortcut created")
            except Exception as e:
                self.log_message.emit(f"[WARNING] Failed to create Linux shortcut: {str(e)}")
