from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from views.modules.app_navigation import (AppNavigationRoutes,
                                               app_navigation)


class Header(QWidget):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        home_button = QPushButton("Home")
        delivery_button = QPushButton("Delivery")

        home_button.clicked.connect(
            lambda: app_navigation.replace(AppNavigationRoutes.MAIN)
        )
        delivery_button.clicked.connect(
            lambda: app_navigation.replace(AppNavigationRoutes.MANAGE_DELIVERY_MAIN)
        )
        
        layout.addWidget(home_button)
        layout.addWidget(delivery_button)

        self.setLayout(layout)
