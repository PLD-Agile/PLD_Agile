from PyQt6.QtWidgets import QHBoxLayout, QLabel, QComboBox, QPushButton, QVBoxLayout
from src.controllers.navigator.page import Page
from PyQt6.QtCore import Qt


class SelectDeliveryManPage(Page):
    def __init__(self):
        super().__init__()

        title_label = QLabel("<b><font size='6'>Select Delivery Man</font></b>")

        delivery_man_label = QLabel("<b>Select Delivery Man:</b>")
        delivery_man_combobox = QComboBox()
        delivery_man_combobox.addItem("John Doe")
        delivery_man_combobox.addItem("Jane Smith")

        select_button = QPushButton("Select")
        select_button.setMaximumWidth(100)

        layout = QVBoxLayout()

        for widget in [title_label, delivery_man_label, delivery_man_combobox]:
            widget.setStyleSheet("color: black;")
            layout.addWidget(widget)

        layout.addWidget(select_button, alignment=Qt.AlignmentFlag.AlignRight)

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
