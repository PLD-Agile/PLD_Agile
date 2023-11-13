from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from src.controllers.navigator.page import Page
from src.views.modules.app_navigator.navigator import get_app_navigator
from src.views.modules.app_navigator.routes import AppNavigationRoutes
from src.views.modules.manage_delivery_man_navigator.navigator import (
    get_manage_delivery_man_navigator,
)
from src.views.modules.manage_delivery_man_navigator.routes import (
    ManageDeliveryManNavigationNames,
    ManageDeliveryManNavigationRoutes,
)
from src.views.ui import Button, Callout, Separator, Text, TextSize
from src.views.ui.button_group import ButtonGroup
from src.views.ui.nav_button import NavigationButton


class ManageDeliveryManPage(Page):
    def __init__(self):
        super().__init__()

        # Define components to be used in this screen
        layout = QVBoxLayout()

        sub_layout_widget = QWidget()
        sub_layout = QHBoxLayout()
        for route in ManageDeliveryManNavigationRoutes:
            name = ManageDeliveryManNavigationNames[route.name].value
            button = Button(name)
            button.clicked.connect(
                lambda _, name=route: get_manage_delivery_man_navigator().replace(name)
            )
            sub_layout.addWidget(button)
        sub_layout_widget.setLayout(sub_layout)

        # Add components in the screen
        layout.addWidget(sub_layout_widget)
        layout.addWidget(get_manage_delivery_man_navigator().get_router_outlet())

        self.setLayout(layout)
