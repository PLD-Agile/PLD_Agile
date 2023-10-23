from PyQt6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from src.controllers.navigator.page import Page
from src.views.modules.main_page_navigation import (
    MainPageNavigationRoutes,
    main_page_navigation,
)
from src.views.main_page.map_view import MapView
from src.views.utils.theme import Theme


class MainPage(Page):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        layout.addWidget(MapView())
        layout.addWidget(main_page_navigation.get_router_outlet())
        
        # layout = QVBoxLayout()

        # sub_layout_widget = QWidget()
        # sub_layout = QHBoxLayout()

        # for route_name in MainPageNavigationRoutes:
        #     button = QPushButton(route_name.name)
        #     button.clicked.connect(
        #         lambda _, name=route_name: main_page_navigation.replace(name)
        #     )
        #     sub_layout.addWidget(button)

        # sub_layout_widget.setLayout(sub_layout)
        # layout.addWidget(sub_layout_widget)

        # layout.addWidget(main_page_navigation.get_router_outlet())

        self.setLayout(layout)
