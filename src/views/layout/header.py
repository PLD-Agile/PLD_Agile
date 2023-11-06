from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from src.views.modules.app_navigator.navigator import get_app_navigator
from src.views.modules.app_navigator.routes import AppNavigationRoutes
from src.views.ui import Button, Callout, Separator, Text, TextSize
from src.views.ui.button_group import ButtonGroup
from src.views.ui.nav_button import NavigationButton


class Header(QWidget):
    def __init__(self):
        super().__init__()

        # Define components to be used in this screen
        layout = QHBoxLayout()
        title = Text("Delivery System v1.0", TextSize.H1)

        home_button = NavigationButton(
            text="Home",
            link=AppNavigationRoutes.MAIN,
            navigator=get_app_navigator(),
        )
        delivery_button = NavigationButton(
            text="Manage Deliverymen",
            link=AppNavigationRoutes.MANAGE_DELIVERY_MAIN,
            navigator=get_app_navigator(),
        )
        button_group = ButtonGroup([home_button, delivery_button])

        # Add components in the screen
        layout.addWidget(title)
        layout.addWidget(button_group)

        self.setLayout(layout)
