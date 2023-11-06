from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from src.controllers.navigator.page import Page
from src.views.modules.app_navigator.navigator import get_app_navigator
from src.views.modules.app_navigator.routes import AppNavigationRoutes
from src.views.modules.manage_delivery_man_navigator.navigator import (
    get_manage_delivery_man_navigator,
)
from src.views.modules.manage_delivery_man_navigator.routes import (
    ManageDeliveryManNavigationRoutes,
)
from src.views.ui import Button, Callout, Separator, Text, TextSize
from src.views.ui.button_group import ButtonGroup
from src.views.ui.nav_button import NavigationButton
from src.services.delivery_man.delivery_man_service import DeliveryManService


class ReadDeliveryMan(Page):
    def __init__(self):
        super().__init__()

        delivery_man_service = DeliveryManService()

        # Define components to be used in this screen
        layout = QVBoxLayout()
        title_label = Text("List of deliverymen", TextSize.H2)

        # Add components in the screen
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(title_label)
        layout.addLayout(self.__build_deliverymen_list(delivery_man_service))

        self.setLayout(layout)

    def __build_deliverymen_list(self, delivery_man_service: DeliveryManService) -> QVBoxLayout:
        deliveryMen = delivery_man_service.get_delivery_men()

        layout = QVBoxLayout()



        for index, deliveryMan in enumerate(deliveryMen.values()):
            deliveryManWidget = Text(str(index+1) + ".  Name: " + deliveryMan.name, TextSize.label)
            layout.addWidget(deliveryManWidget)

        return layout