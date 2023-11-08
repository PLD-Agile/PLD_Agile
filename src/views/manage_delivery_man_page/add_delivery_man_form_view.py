from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout

from src.controllers.navigator.page import Page
from src.views.ui import Button, Callout, Separator, Text, TextSize


class AddDeliveryManFormView(Page):
    def __init__(self):
        super().__init__()

        # Define components to be used in this screen
        layout = QVBoxLayout()
        title_label = Text("Create a deliveryman", TextSize.H2)

        name_label = Text("Name", TextSize.label)
        name_input = QLineEdit()

        buttons_layout = QHBoxLayout()
        add_button = Button("Create")

        # Add components in the screen
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(title_label)
        layout.addWidget(name_label)
        layout.addWidget(name_input)

        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)
        buttons_layout.addWidget(add_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)
