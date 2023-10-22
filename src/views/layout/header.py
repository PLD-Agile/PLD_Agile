from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from views.modules.app_navigation import AppNavigationRoutes, app_navigation
from src.views.ui.nav_button import NavigationButton
from src.views.ui.button_group import ButtonGroup


class Header(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        title = QLabel("PLD Agile")

        home_button = NavigationButton(
            text="Home",
            link=AppNavigationRoutes.MAIN,
            navigator=app_navigation,
        )
        delivery_button = NavigationButton(
            text="Delivery",
            link=AppNavigationRoutes.MANAGE_DELIVERY_MAIN,
            navigator=app_navigation,
        )

        button_group = ButtonGroup([home_button, delivery_button])

        layout.addWidget(title)
        layout.addWidget(button_group)

        self.setLayout(layout)
