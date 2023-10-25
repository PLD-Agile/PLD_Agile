from PyQt6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
from src.controllers.navigator.page import Page
from PyQt6.QtCore import Qt

class AddDeliveryManFormView(Page):
    def __init__(self):
        super().__init__()

        title_label = QLabel("<b><font size='6'>Add Delivery Man</font></b>")

        name_label = QLabel("<b>Name:</b>")
        name_input = QLineEdit()

        phone_label = QLabel("<b>Phone:</b>")
        phone_input = QLineEdit()

        add_button = QPushButton("Add Delivery Man")
        add_button.setFixedWidth(150)  

        layout = QVBoxLayout()

        for widget in [title_label, name_label, name_input, phone_label, phone_input]:
            widget.setStyleSheet("color: black;")
            layout.addWidget(widget)

        layout.addWidget(add_button, alignment=Qt.AlignmentFlag.AlignRight)

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
