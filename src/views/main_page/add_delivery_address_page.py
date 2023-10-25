from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
from src.controllers.navigator.page import Page

class AddDeliveryAddressPage(Page):
    def __init__(self):
        super().__init__()

        self.address_label = QLabel("<b>Delivery Address:</b>")
        self.address_input = QLineEdit()
        self.add_address_button = QPushButton("Add Address")
        self.add_address_button.clicked.connect(self.add_address)

        layout = QVBoxLayout()

        for widget in [self.address_label, self.address_input, self.add_address_button]:
            widget.setStyleSheet("color: black;")
            layout.addWidget(widget)

        style_sheet = """
            QPushButton {
                background-color: #FFC0CB;  /* Pink */
                border: none;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #FF69B4;  /* Hot Pink on hover */
            }
        """
        self.setStyleSheet(style_sheet)

        self.setLayout(layout)

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
