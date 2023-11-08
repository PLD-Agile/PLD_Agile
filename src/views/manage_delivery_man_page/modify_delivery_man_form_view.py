from typing import Dict
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QLineEdit, QComboBox, QLayout, QCheckBox
from models.delivery_man.delivery_man import DeliveryMan
from services.delivery_man.delivery_man_service import DeliveryManService

from src.controllers.navigator.page import Page
from src.views.ui import Button, Callout, Separator, Text, TextSize


class ModifyDeliveryManFormView(Page):
    __delivery_man_control: QComboBox
    __name_input: QLineEdit

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
        name_input = QLineEdit()
        delivery_man_label = QLabel("Delivery man")
        self.__availabilities_checkboxes = [QCheckBox(f"Availability {i}") for i in range(8, 12)]
        modify_button = Button("Modify")
        
        modify_button.clicked.connect(self.__modify_delivery_man)
        
        # Add components in the screen
        delivery_man_layout.addWidget(delivery_man_label)
        delivery_man_layout.addWidget(delivery_man_combobox)
        
        input_layout = QHBoxLayout()
        name_layout = QVBoxLayout()
        availabilities_layout = QVBoxLayout()
        
        name_label = QLabel("Name")
        name_layout.addWidget(name_label)
        name_layout.addWidget(name_input)

        availabilities_label = QLabel("Availabilities")
        availabilities_layout.addWidget(availabilities_label)

        for checkbox in self.__availabilities_checkboxes:
            availabilities_layout.addWidget(checkbox)

        input_layout.addLayout(name_layout)
        input_layout.addLayout(availabilities_layout)
        
        delivery_man_layout.addLayout(input_layout)
        delivery_man_layout.addWidget(modify_button)

        delivery_man_layout.setContentsMargins(0, 0, 0, 0)
        delivery_man_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.__delivery_man_control = delivery_man_combobox

        return delivery_man_layout

    def __modify_delivery_man(self):
        selected_delivery_man = self.__delivery_man_control.currentData()
        if not selected_delivery_man:
            return

        name = self.__name_input.text
        availabilities = [i for i in range(8, 12) if self.__availabilities_checkboxes[i - 8].isChecked()]

        if not name and not availabilities:
            return  # No changes were made

        delivery_man_info = {"name": name, "availabilities": availabilities}
        modified_delivery_man = DeliveryManService.instance().modify_delivery_man(selected_delivery_man, delivery_man_info)

        # Show a popup with the changes
        message = f"Delivery Man '{selected_delivery_man.name}' modified. New name: {modified_delivery_man.name}, New availabilities: {modified_delivery_man.availabilities}"
        popup = Callout("Success", message)
        popup.exec()
    
    def __update_delivery_man_combobox(self, delivery_men: Dict[str, DeliveryMan]) -> None:
        current_value = self.__delivery_man_control.currentData()
        self.__delivery_man_control.clear()

        for delivery_man in delivery_men.values():
            self.__delivery_man_control.addItem(delivery_man.name, delivery_man)

        new_index = max(self.__delivery_man_control.findData(current_value), 0)

        self.__delivery_man_control.setCurrentIndex(new_index)

        self.findChild(QLineEdit).text = self.__delivery_man_control.currentText
