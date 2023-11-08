from typing import Dict
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget, QComboBox, QLayout
from models.delivery_man.delivery_man import DeliveryMan
from services.delivery_man.delivery_man_service import DeliveryManService

from src.controllers.navigator.page import Page
from src.views.ui import Button, Callout, Separator, Text, TextSize


class ModifyDeliveryManFormView(Page):
    __delivery_man_control: QComboBox

    def __init__(self):
        super().__init__()

        # Define components to be used in this screen
        layout = QVBoxLayout()
        title_label = Text("Modify a deliveryman", TextSize.H2)

        # Add components in the screen
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(title_label)
        layout.addLayout(self.__build_delivery_man_combobox())

        self.setLayout(layout)

        DeliveryManService.instance().delivery_men.subscribe(self.__update_delivery_man_combobox)

    def __build_delivery_man_combobox(self) -> QLayout:
        delivery_man_layout = QVBoxLayout()
        delivery_man_combobox = QComboBox()
        delivery_man_label = Text("Delivery man", TextSize.label)

        # Add components in the screen
        delivery_man_layout.addWidget(delivery_man_label)
        delivery_man_layout.addWidget(delivery_man_combobox)

        delivery_man_layout.setContentsMargins(0, 0, 0, 0)
        delivery_man_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.__delivery_man_control = delivery_man_combobox

        return delivery_man_layout
    
    def __update_delivery_man_combobox(self, delivery_men: Dict[str, DeliveryMan]) -> None:
        current_value = self.__delivery_man_control.currentData()
        self.__delivery_man_control.clear()

        for delivery_man in delivery_men.values():
            self.__delivery_man_control.addItem(delivery_man.name, delivery_man)

        new_index = max(self.__delivery_man_control.findData(current_value), 0)

        self.__delivery_man_control.setCurrentIndex(new_index)
