from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QScrollArea, QFrame, QWidget, QVBoxLayout
from gui.components.header import HeaderComponent
from gui.components.footer import FooterComponent
from gui.views.node_setup_view import NodeSetupView
from gui.sections.hero_section import create_hero_section
from gui.sections.networks_section import create_networks_section
from gui.sections.action_buttons import create_action_buttons


class DashboardView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Header (only shown in dashboard view)
        self.header = HeaderComponent("Polaris Miner Node")
        self.layout.addWidget(self.header)

        # Stacked widget to switch between views
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Dashboard view
        self.dashboard_view = QWidget()
        dashboard_layout = QVBoxLayout(self.dashboard_view)
        dashboard_layout.setContentsMargins(0, 0, 0, 0)

        # Scrollable content area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(10)

        # Sections
        self.content_layout.addWidget(create_hero_section())
        self.content_layout.addWidget(create_networks_section())
        self.content_layout.addWidget(create_action_buttons(self.toggle_view_to_node_setup))
        self.content_layout.addStretch()
        self.content_layout.addWidget(FooterComponent("PolarisCloud", "v1.0.0"))

        scroll_area.setWidget(content_widget)
        dashboard_layout.addWidget(scroll_area)

        # Node setup view (register + advanced)
        self.node_setup_view = NodeSetupView()

        # Add both views
        self.stacked_widget.addWidget(self.dashboard_view)
        self.stacked_widget.addWidget(self.node_setup_view)

        # Start on dashboard view
        self.stacked_widget.setCurrentWidget(self.dashboard_view)

    def toggle_view_to_node_setup(self):
        """Switch to the node setup screen and hide the header"""
        self.header.hide()
        self.stacked_widget.setCurrentWidget(self.node_setup_view)

    def toggle_view_to_dashboard(self):
        """Switch back to dashboard and show the header"""
        self.header.show()
        self.stacked_widget.setCurrentWidget(self.dashboard_view)
