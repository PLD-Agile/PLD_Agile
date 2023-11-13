from typing import Dict, List
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QVBoxLayout, QLineEdit, QComboBox, QLayout, QCheckBox
from models.delivery_man.delivery_man import DeliveryMan
from src.services.delivery_man.delivery_man_service import DeliveryManService

from src.controllers.navigator.page import Page
from src.views.ui import Button, Text, TextSize


class ModifyDeliveryManFormView(Page):
    __delivery_man_control: QComboBox
    __name_input: QLineEdit
    __availabilities_checkboxes: List[QCheckBox]

    def __init__(self):
        super().__init__()

        # Define components to be used in this screen
        layout = QVBoxLayout()
        title_label = Text("Modify a deliveryman", TextSize.H2)
        modify_button = Button("Modify")

        modify_button.clicked.connect(self.__modify_delivery_man)

        # Add components in the screen
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(title_label)
        layout.addLayout(self.__build_delivery_man_combobox())
        layout.addLayout(self.__build_delivery_man_inputs())

        layout.addWidget(modify_button)

        self.setLayout(layout)

        DeliveryManService.instance().delivery_men.subscribe(self.__update_delivery_man_combobox)

    def __build_delivery_man_combobox(self) -> QLayout:
        delivery_man_combobox_layout = QVBoxLayout()
        delivery_man_label = QLabel("Delivery man")
        self.__delivery_man_control = QComboBox()
        
        # Add components in the screen
        delivery_man_combobox_layout.addWidget(delivery_man_label)
        delivery_man_combobox_layout.addWidget(self.__delivery_man_control)

        delivery_man_combobox_layout.setContentsMargins(0, 0, 0, 0)
        delivery_man_combobox_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.__delivery_man_control.currentIndexChanged.connect(
            lambda: self.__update_delivery_man_inputs(self.__delivery_man_control.currentData())
        )

        return delivery_man_combobox_layout
    
    def __build_delivery_man_inputs(self) -> QLayout:
        input_layout = QHBoxLayout()
        name_layout = QVBoxLayout()
        availabilities_layout = QVBoxLayout()
        availabilities_label = QLabel("Availabilities")
        name_label = QLabel("Name")
        self.__name_input = QLineEdit()
        self.__availabilities_checkboxes = [QCheckBox(f"{i} am") for i in range(8, 12)]
        
        input_layout = QHBoxLayout()
        name_layout = QVBoxLayout()
        availabilities_layout = QVBoxLayout()
        
        # Add components in the screen
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.__name_input)

        availabilities_layout.addWidget(availabilities_label)

        for checkbox in self.__availabilities_checkboxes:
            availabilities_layout.addWidget(checkbox)

        input_layout.addLayout(name_layout)
        input_layout.addLayout(availabilities_layout)

        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        return input_layout

    def __modify_delivery_man(self):
        selected_delivery_man = self.__delivery_man_control.currentData()
        if not selected_delivery_man:
            return

        name = self.__name_input.text()
        availabilities = [i for i in range(8, 12) if self.__availabilities_checkboxes[i - 8].isChecked()]

        if name == selected_delivery_man.name and availabilities == selected_delivery_man.availabilities:
            return  # No changes were made

        delivery_man_info = {"name": name, "availabilities": availabilities}
        modified_delivery_man = DeliveryManService.instance().modify_delivery_man(selected_delivery_man, delivery_man_info)

        # Show a popup with the changes
        message_box = QMessageBox()
        message_box.setWindowTitle("Success")
        message_box.setText(f"Delivery man '{modified_delivery_man.name}' modified successfully.")
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        message_box.exec()
    
    def __update_delivery_man_combobox(self, delivery_men: Dict[str, DeliveryMan]) -> None:
        current_value = self.__delivery_man_control.currentData()
        self.__delivery_man_control.clear()

        for delivery_man in delivery_men.values():
            self.__delivery_man_control.addItem(delivery_man.name, delivery_man)

        new_index = max(self.__delivery_man_control.findData(current_value), 0)

        self.__delivery_man_control.setCurrentIndex(new_index)

    def __update_delivery_man_inputs(self, delivery_man: DeliveryMan) -> None:
        if delivery_man is not None:
            self.__name_input.setText(delivery_man.name)
            # Uncheck all checkboxes
            for checkbox in self.__availabilities_checkboxes:
                checkbox.setChecked(False)

            # Check checkboxes based on delivery man's availabilities
            for availability in delivery_man.availabilities:
                index = availability - 8
                if 0 <= index < len(self.__availabilities_checkboxes):
                    self.__availabilities_checkboxes[index].setChecked(True)