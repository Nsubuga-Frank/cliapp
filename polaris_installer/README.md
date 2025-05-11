# Polaris Miner Node

A GUI application for managing Bittensor wallets and miners on the Polaris subnet.

## Features

- **Wallet Management**: View and manage Bittensor wallets
- **Subnet Registration**: Register wallets to subnet 49 (Polaris)
- **UID Lookup**: Check if your wallet is registered on the subnet and get your miner UID
- **Miner Control**: Start and stop your miner directly from the GUI

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```

## Requirements

- Python 3.8+
- Bittensor 6.0.0+
- PySide6 6.4.0+

## Wallet Setup Process

The application guides you through a 5-step setup process:

1. **System Info**: Detects your system configuration and network settings
2. **Network**: Select the blockchain network (currently only Bittensor is active)
3. **Wallet**: Manage your wallets and check registration status
4. **Subnet**: Configure subnet details and control your miner
5. **Register**: Complete the registration process

## Bittensor Integration

The application integrates with Bittensor through:

- Direct API calls using the `bittensor` Python package
- Command-line operations using `btcli` for wallet registration and mining
- Background processes for mining operations

## Usage

1. Start the application
2. Navigate through the setup steps
3. Select or create a wallet
4. Register your wallet to subnet 49 (if not already registered)
5. Start mining

## Development

The application is built with:

- PySide6 for the GUI
- Bittensor for blockchain interactions
- Python threading for non-blocking operations

## License

MIT License 