from PySide6.QtWidgets import QWidget, QHBoxLayout
from gui.components.network_card import NetworkCard

def create_networks_section():
    section = QWidget()
    layout = QHBoxLayout(section)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(10)

    layout.addWidget(NetworkCard(
        "Commune",
        "Provide your GPU by connecting to Polaris via CommuneAI. Rewarded in SCOMAI.",
        True,
        "gray"
    ))

    layout.addWidget(NetworkCard(
        "Bittensor",
        "Provide your GPU via Bittensor. Rewarded in STAO.",
        True,
        "blue"
    ))

    layout.addWidget(NetworkCard(
        "Tokenomics",
        "A new ecosystem for decentralized AI.",
        False,
        "yellow"
    ))

    return section
