from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from src.views.modules.main_navigation import (MainNavigationRoutes,
                                               main_navigation)


class Header(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        home_button = QPushButton("Home")
        delivery_button = QPushButton("Delivery")

        home_button.clicked.connect(
            lambda: main_navigation.replace(MainNavigationRoutes.MAIN)
        )
        delivery_button.clicked.connect(
            lambda: main_navigation.replace(MainNavigationRoutes.MANAGE_DELIVERY_MAIN)
        )
        
        layout.addWidget(home_button)
        layout.addWidget(delivery_button)

        self.setLayout(layout)
