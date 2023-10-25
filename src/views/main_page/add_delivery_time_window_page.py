from PyQt6.QtWidgets import QHBoxLayout, QLabel, QComboBox, QPushButton, QVBoxLayout
from src.controllers.navigator.page import Page

class AddDeliveryTimeWindowPage(Page):
    def __init__(self):
        super().__init__()

        title_label = QLabel("<b><font size='6'>Add Delivery Time Window</font></b>")

        courier_label = QLabel("<b>Courier Name:</b>")
        courier_combobox = QComboBox()
        courier_combobox.addItem("John Doe")
        courier_combobox.addItem("Jane Smith")

        delivery_point_label = QLabel("<b>Delivery Point:</b>")
        delivery_point_combobox = QComboBox()
        delivery_point_combobox.addItem("123 Main Street")
        delivery_point_combobox.addItem("456 Elm Avenue")

        time_window_label = QLabel("<b>Time Window:</b>")
        time_window_combobox = QComboBox()
        time_window_combobox.addItem("8:00 AM - 9:00 AM")
        time_window_combobox.addItem("9:00 AM - 10:00 AM")
        time_window_combobox.addItem("10:00 AM - 11:00 AM")
        time_window_combobox.addItem("11:00 AM - 12:00 PM")

        add_button = QPushButton("Add Delivery Request")

        layout = QVBoxLayout()

        for label in [title_label, courier_label, courier_combobox, delivery_point_label, delivery_point_combobox, time_window_label, time_window_combobox]:
            label.setStyleSheet("color: black;")
            layout.addWidget(label)

        layout.addWidget(add_button)

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
