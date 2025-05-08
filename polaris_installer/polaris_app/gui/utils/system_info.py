import platform
import socket
import subprocess
import os
import shutil
import re
import getpass
import json
import psutil
import requests


def get_full_system_info(username=None, open_ports=None):
    """
    Gathers system information. Username and open_ports can be provided by user.
    If not provided, defaults are used for username, and open ports are detected.
    """
    # System identification
    hostname = socket.gethostname()
    try:
        public_ip = requests.get('https://api.ipify.org').text.strip()
    except:
        public_ip = "Unavailable"

    try:
        ip_address = socket.gethostbyname(hostname)
    except:
        ip_address = "127.0.0.1"

    # OS information
    os_name = f"{platform.system()} {platform.release()}"

    # CPU information
    cpu_info = {
        "model": platform.processor(),
        "cores": psutil.cpu_count(logical=False),
        "threads": psutil.cpu_count(logical=True),
        "frequency": f"{psutil.cpu_freq().current:.2f} MHz" if psutil.cpu_freq() else "Unknown"
    }

    # Memory and storage
    memory = f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB"
    storage = _get_disk_info()
    
    # GPU information
    gpus = _get_gpu_info()
    
    # Use provided username or get current user as fallback
    if not username:
        username = getpass.getuser()
    
    # User can specify open ports or we'll detect them
    if not open_ports:
        detected_ports = _get_open_ports()
        open_ports = detected_ports[:2] if detected_ports else ["22", "8080"]
    
    # Ensure ports is a list of strings
    if isinstance(open_ports, (list, tuple)):
        open_ports = [str(port) for port in open_ports]
    else:
        open_ports = [str(open_ports)]
    
    # SSH connection string (using the first open port if available)
    ssh_port = open_ports[0] if open_ports else "22"
    ssh_conn = f"ssh://{username}@{public_ip}:{ssh_port}"

    return [{
        "hostname": hostname,
        "operating_system": os_name,
        "ip_address": ip_address,
        "public_ip": public_ip,
        "compute_resources": [{
            "id": "resource1",
            "resource_type": "CPU",
            "location": "Local Machine",
            "hourly_price": 1.0,
            "ram": memory,
            "storage": storage,
            "network": {
                "internal_ip": ip_address,
                "public_ip": public_ip,
                "ssh": ssh_conn,
                "open_ports": open_ports,
                "username": username,
                "auth_type": "public_key"
            },
            "cpu_specs": cpu_info,
            "gpu_specs": gpus
        }]
    }]


def _get_disk_info():
    try:
        total, used, free = shutil.disk_usage("/")
        return {
            "type": "SSD/HDD",
            "capacity": f"{round(total / (1024 ** 3), 2)} GB"
        }
    except:
        return {"type": "Unknown", "capacity": "Unknown"}


def _get_gpu_info():
    gpus = []
    try:
        result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], 
                                capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.strip().splitlines():
                name, mem = line.split(",", 1)
                gpus.append({
                    "model": name.strip(),
                    "vram": mem.strip(),
                    "cuda_cores": 8704  # Default CUDA cores value
                })
    except:
        pass
    return gpus


def _get_open_ports():
    try:
        result = subprocess.run(["ss", "-tuln"], capture_output=True, text=True)
        ports = re.findall(r":(\d+)\s", result.stdout)
        return sorted(set(ports))
    except:
        return []
