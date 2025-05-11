import json
import os
import signal
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
import logging

# Configure logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Try to import bittensor
try:
    import bittensor as bt
    BITTENSOR_AVAILABLE = True
except ImportError:
    BITTENSOR_AVAILABLE = False
    logger.warning("Bittensor not installed. Some functionality will be limited.")

# Constants
POLARIS_HOME = Path.home() / '.polaris'
BITTENSOR_CONFIG_PATH = POLARIS_HOME / 'bittensor'
PID_FILE = BITTENSOR_CONFIG_PATH / 'pids' / 'miner.pid'
LOG_FILE = BITTENSOR_CONFIG_PATH / 'logs' / 'miner.log'

def setup_directories():
    """Create necessary directories if they don't exist"""
    POLARIS_HOME.mkdir(parents=True, exist_ok=True)
    BITTENSOR_CONFIG_PATH.mkdir(parents=True, exist_ok=True)
    (BITTENSOR_CONFIG_PATH / 'pids').mkdir(parents=True, exist_ok=True)
    (BITTENSOR_CONFIG_PATH / 'logs').mkdir(parents=True, exist_ok=True)

def load_config():
    """Load miner configuration from file"""
    try:
        with open(BITTENSOR_CONFIG_PATH / 'config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error("Configuration file not found. Please run registration first.")
        return None
    except json.JSONDecodeError:
        logger.error("Invalid configuration file.")
        return None

def save_config(config):
    """Save miner configuration to file"""
    setup_directories()
    with open(BITTENSOR_CONFIG_PATH / 'config.json', 'w') as f:
        json.dump(config, f, indent=4)

def get_subtensor(network='finney'):
    """Initialize and return subtensor connection"""
    if not BITTENSOR_AVAILABLE:
        logger.error("Bittensor not installed.")
        return None
        
    try:
        subtensor = bt.subtensor(network=network)
        return subtensor
    except Exception as e:
        logger.error(f"Failed to connect to subtensor: {str(e)}")
        return None

def write_pid(pid):
    """Write process ID to file"""
    setup_directories()
    with open(PID_FILE, 'w') as f:
        f.write(str(pid))

def remove_pid():
    """Remove PID file"""
    try:
        PID_FILE.unlink()
    except FileNotFoundError:
        pass

def log_message(message):
    """Write message to log file"""
    setup_directories()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{timestamp}] {message}\n")

def start_bittensor_miner(wallet_name, hotkey="default", netuid=49, network="finney"):
    """Start the Bittensor miner process"""
    if PID_FILE.exists():
        logger.warning("Miner process is already running.")
        return False, "Miner process is already running."

    setup_directories()
    
    try:
        # Start the miner process
        process = subprocess.Popen(
            [
                'btcli', 'run',
                '--wallet.name', wallet_name,
                '--wallet.hotkey', hotkey,
                '--netuid', str(netuid),
                '--subtensor.network', network,
                '--logging.debug'
            ],
            stdout=open(LOG_FILE, 'a'),
            stderr=subprocess.STDOUT,
            start_new_session=True
        )
        
        # Write PID to file
        write_pid(process.pid)
        
        message = f"Started Bittensor miner (PID: {process.pid})"
        logger.info(message)
        log_message(f"Started miner process with PID {process.pid}")
        
        return True, message
        
    except Exception as e:
        error_msg = f"Failed to start miner: {str(e)}"
        logger.error(error_msg)
        log_message(error_msg)
        return False, error_msg

def stop_bittensor_miner():
    """Stop the Bittensor miner process"""
    try:
        if not PID_FILE.exists():
            logger.warning("No running miner process found.")
            return True, "No running miner process found."

        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())

        # Try to kill the process
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
            time.sleep(2)  # Give it some time to shutdown gracefully
            
            # Force kill if still running
            if os.kill(pid, 0):
                os.killpg(os.getpgid(pid), signal.SIGKILL)
                
        except ProcessLookupError:
            pass  # Process already terminated
        
        remove_pid()
        log_message("Stopped miner process")
        return True, "Stopped miner process"
        
    except Exception as e:
        error_msg = f"Failed to stop miner: {str(e)}"
        logger.error(error_msg)
        log_message(error_msg)
        return False, error_msg

def check_miner_status():
    """Check the status of the miner process"""
    if not PID_FILE.exists():
        return False
        
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
            
        # Check if process is running
        os.kill(pid, 0)
        return True
    except (ProcessLookupError, FileNotFoundError):
        remove_pid()
        return False
    except Exception:
        return False

def is_bittensor_running():
    """Alias function for checking if the Bittensor miner is running"""
    return check_miner_status()

def get_uid_from_hotkey(hotkey, netuid=49, network="finney"):
    """
    Retrieve the UID for a wallet registered on a subnet using its hotkey.

    Args:
        hotkey (str): The public key (hotkey) of the wallet.
        netuid (int): The subnet ID.
        network (str): The network to connect to ('finney' for mainnet, 'test' for testnet)

    Returns:
        tuple: (success, result_dict) where result_dict contains uid if successful
    """
    if not BITTENSOR_AVAILABLE:
        return False, {"error": "Bittensor not installed"}
        
    # Create logs directory if it doesn't exist
    setup_directories()
    logs_dir = BITTENSOR_CONFIG_PATH / 'logs'
    
    # Path for the UID log file
    uid_log_file = logs_dir / 'miner_uid_log.txt'
    
    # Log the attempt to retrieve UID
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': 'get_uid_attempt',
        'hotkey': hotkey,
        'netuid': netuid,
        'network': network
    }
    
    try:
        # Connect to the subtensor network
        sub = bt.subtensor(network)
        logger.info(f"Connected to {network} network")

        # Get the metagraph for the subnet
        meta = sub.metagraph(netuid)
        logger.info(f"Retrieved metagraph for subnet {netuid}")
        
        # Ensure we're using the actual SS58 address
        if not hotkey.startswith('5'):
            # If not an SS58 address, try to get it from wallet
            try:
                wallet = bt.wallet(name=hotkey, hotkey="default")
                hotkey = wallet.hotkey.ss58_address
            except:
                # If that fails too, log warning
                logger.warning(f"Provided hotkey '{hotkey}' does not appear to be an SS58 address")
                log_entry['error'] = "Not an SS58 address"
                with open(uid_log_file, 'a') as f:
                    f.write(json.dumps(log_entry) + '\n')
                return False, {"error": "Not a valid SS58 address"}
            
        # Find the UID for the given hotkey
        uid = next((uid for uid, registered_hotkey in zip(meta.uids, meta.hotkeys) if registered_hotkey == hotkey), None)

        if uid is not None:
            logger.info(f"Found UID {uid} for hotkey {hotkey[:10]}...")
            
            # Update log entry with success info
            log_entry['status'] = 'success'
            log_entry['uid'] = int(uid)
            
            # Write to log file
            with open(uid_log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')
                
            # Also write to a dedicated file for this specific hotkey
            hotkey_uid_file = logs_dir / f'hotkey_{hotkey[:10]}_uid.txt'
            with open(hotkey_uid_file, 'w') as f:
                f.write(f"Hotkey: {hotkey}\nUID: {uid}\nNetwork: {network}\nNetuid: {netuid}\nTimestamp: {datetime.now().isoformat()}")
                
            return True, {"uid": int(uid), "hotkey": hotkey, "netuid": netuid, "network": network}
        else:
            logger.warning(f"Could not find UID for hotkey {hotkey[:10]}... in subnet {netuid}")
            
            # Update log entry with failure info
            log_entry['status'] = 'not_found'
            
            # Write to log file
            with open(uid_log_file, 'a') as f:
                f.write(json.dumps(log_entry) + '\n')

            return False, {"error": "Hotkey not found in subnet"}
        
    except Exception as e:
        logger.error(f"Error retrieving UID: {str(e)}")
        
        # Update log entry with error info
        log_entry['status'] = 'error'
        log_entry['error_message'] = str(e)
        
        # Write to log file
        with open(uid_log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
            
        return False, {"error": str(e)}

def register_wallet_to_subnet(wallet_name, hotkey="default", netuid=49, network="finney"):
    """
    Register a wallet to a subnet using btcli.
    
    Args:
        wallet_name (str): The name of the wallet
        hotkey (str): The hotkey name
        netuid (int): The subnet ID
        network (str): The network name
        
    Returns:
        tuple: (success, message)
    """
    try:
        # Run the btcli command to register
        cmd = [
            "btcli", "subnets", "register",
            "--wallet.name", wallet_name,
            "--wallet.hotkey", hotkey,
            "--netuid", str(netuid),
            "--network", network
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            logger.info(f"Successfully registered wallet {wallet_name} to subnet {netuid}")
            return True, stdout
        else:
            logger.error(f"Failed to register wallet: {stderr}")
            return False, stderr
            
    except Exception as e:
        logger.error(f"Error during wallet registration: {str(e)}")
        return False, str(e)

def list_wallets():
    """
    List all available wallets.
    
    Returns:
        list: List of wallet names
    """
    if not BITTENSOR_AVAILABLE:
        return []
        
    try:
        return bt.wallet.list_wallets()
    except Exception as e:
        logger.error(f"Error listing wallets: {str(e)}")
        return []

def get_wallet_info(wallet_name, hotkey="default"):
    """
    Get information about a wallet.
    
    Args:
        wallet_name (str): The name of the wallet
        hotkey (str): The hotkey name
        
    Returns:
        dict: Wallet information
    """
    if not BITTENSOR_AVAILABLE:
        return {"error": "Bittensor not installed"}
        
    try:
        wallet = bt.wallet(name=wallet_name, hotkey=hotkey)
        return {
            "coldkey": wallet.coldkey.ss58_address,
            "hotkey": wallet.hotkey.ss58_address,
            "coldkeypub": wallet.coldkeypub.ss58_address
        }
    except Exception as e:
        logger.error(f"Error getting wallet info: {str(e)}")
        return {"error": str(e)} 