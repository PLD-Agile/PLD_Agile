from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from src.controllers.navigator.page import Page
from src.views.modules.manage_delivery_man_navigator.navigator import (
    get_manage_delivery_man_navigator,
)
from src.views.modules.manage_delivery_man_navigator.routes import (
    ManageDeliveryManNavigationRoutes,
)


class ManageDeliveryManPage(Page):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        sub_layout_widget = QWidget()
        sub_layout = QHBoxLayout()

        for route_name in ManageDeliveryManNavigationRoutes:
            button = QPushButton(route_name.name)
            button.clicked.connect(
                lambda _, name=route_name: get_manage_delivery_man_navigator().replace(
                    name
                )
            )
            sub_layout.addWidget(button)

        sub_layout_widget.setLayout(sub_layout)
        layout.addWidget(sub_layout_widget)

        layout.addWidget(get_manage_delivery_man_navigator().get_router_outlet())

        self.setLayout(layout)
