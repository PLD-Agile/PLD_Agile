from PyQt6.QtWidgets import QHBoxLayout, QPushButton
from src.controllers.navigator.page import Page

class ConfirmDeliveryAddressPage(Page):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        self.confirm_button = QPushButton("Confirm Address")
        self.confirm_button.clicked.connect(self.confirm_address)
        self.confirm_button.setStyleSheet(
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

        layout.addWidget(self.confirm_button)

        self.setLayout(layout)

    def confirm_address(self):
        print("Address confirmed!")
