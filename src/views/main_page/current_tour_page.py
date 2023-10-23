from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from src.controllers.navigator.page import Page

class CurrentTourPage(Page):
    def __init__(self):
        super().__init__()

        title_label = QLabel("<b><font size='6'>Details of Route</font></b>")
        courier_label = QLabel("<b>Courier Name:</b> Lopez J")
        next_delivery_label = QLabel("<b>Next Delivery Point:</b> 61 Avenue Roger Salengro")
        estimated_time_label = QLabel("<b>Estimated Time:</b> 4 minutes")
        time_to_warehouse_label = QLabel("<b>Time to Warehouse:</b> 2 minutes")
        route_length_label = QLabel("<b>Route Length:</b> 15 meters")

        return_button = QPushButton("Return")
        return_button.setMaximumWidth(100)

        layout = QVBoxLayout()

        for label in [title_label, courier_label, next_delivery_label, estimated_time_label, time_to_warehouse_label, route_length_label]:
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label.setStyleSheet("color: black;")
            layout.addWidget(label)

        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addSpacerItem(spacer)

        layout.addWidget(return_button, alignment=Qt.AlignmentFlag.AlignRight)

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
