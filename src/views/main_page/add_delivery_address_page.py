from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
from src.controllers.navigator.page import Page

class AddDeliveryAddressPage(Page):
    def __init__(self):
        super().__init__()

        self.address_label = QLabel("Delivery Address:")
        self.address_input = QLineEdit()
        self.add_address_button = QPushButton("Add Address")
        self.add_address_button.clicked.connect(self.add_address)
        self.add_address_button.setStyleSheet(
            "QPushButton {"
                "background-color: #FFD1DC;"  
                "border: none;"
                "color: white;"
                "padding: 10px 20px;"
                "text-align: center;"
                "text-decoration: none;"
                "display: inline-block;"
                "font-size: 16px;"
                "margin: 4px 2px;"
                "cursor: pointer;"
                "border-radius: 8px;"
            "}"
            "QPushButton:hover {"
                "background-color: #FFB6C1;"  
            "}"
        )

        layout = QVBoxLayout()

        layout.addWidget(self.address_label)
        layout.addWidget(self.address_input)
        layout.addWidget(self.add_address_button)

        self.setLayout(layout)

        self.address_list = []

    def add_address(self):
        address = self.address_input.text()

        if address:
            self.address_list.append(address)
            print(f"Added address: {address}")
        else:
            print("Invalid address provided!")

        self.address_input.clear()

    def get_address_list(self):
        return self.address_list
