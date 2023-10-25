from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from src.views.modules.app_navigator.navigator import get_app_navigator
from src.views.modules.app_navigator.routes import AppNavigationRoutes
from src.views.ui.button_group import ButtonGroup
from src.views.ui.nav_button import NavigationButton


class Header(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        title = QLabel("PLD Agile")

        home_button = NavigationButton(
            text="Home",
            link=AppNavigationRoutes.MAIN,
            navigator=get_app_navigator(),
        )
        delivery_button = NavigationButton(
            text="Delivery",
            link=AppNavigationRoutes.MANAGE_DELIVERY_MAIN,
            navigator=get_app_navigator(),
        )

        button_group = ButtonGroup([home_button, delivery_button])

        layout.addWidget(title)
        layout.addWidget(button_group)

        self.setLayout(layout)
