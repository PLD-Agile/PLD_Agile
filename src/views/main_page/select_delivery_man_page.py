from PyQt6.QtWidgets import QHBoxLayout, QLabel

from src.controllers.navigator.page import Page


class SelectDeliveryManPage(Page):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        layout.addWidget(QLabel("SelectDeliveryManPage works!"))

        self.setLayout(layout)
