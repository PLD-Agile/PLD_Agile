from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLayout,
    QPushButton,
    QSizePolicy,
    QStyle,
    QVBoxLayout,
    QWidget,
)

from src.controllers.navigator.page import Page
from views.main_page.map.map_view import MapView
from src.views.modules.main_page_navigation import (
    MainPageNavigationRoutes,
    main_page_navigation,
)
from src.views.ui.button import Button
from src.views.ui.button_group import ButtonGroup
from src.views.utils.theme import Theme
from typing import List, Tuple


class MainPage(Page):
    def __init__(self):
        super().__init__()

        layout = QHBoxLayout()

        layout.addLayout(self.__build_map_view())
        layout.addWidget(main_page_navigation.get_router_outlet())

        self.setLayout(layout)

    def __build_map_view(self) -> QLayout:
        map_layout = QVBoxLayout()
        map_view = MapView()

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        reset_map_button, map_zoom_out_button, map_zoom_in_button = self.__build_map_action_buttons(map_view)
        map_zoom_buttons = ButtonGroup([map_zoom_out_button, map_zoom_in_button])
        
        buttons_layout.addWidget(reset_map_button)
        buttons_layout.addWidget(map_zoom_buttons)

        map_layout.addWidget(map_view)
        map_layout.addLayout(buttons_layout)

        return map_layout

    def __build_map_action_buttons(self, map_view: MapView) -> Tuple[QWidget]:
        reset_map_button = Button("Reset zoom")
        map_zoom_out_button = Button(icon="minus")
        map_zoom_in_button = Button(icon="plus")
        
        reset_map_button.clicked.connect(map_view.fit_map)
        map_zoom_out_button.clicked.connect(map_view.zoom_out)
        map_zoom_in_button.clicked.connect(map_view.zoom_in)
        
        map_view.ready.subscribe(lambda ready: [button.setDisabled(not ready) for button in [reset_map_button, map_zoom_out_button, map_zoom_in_button]])
        
        return reset_map_button, map_zoom_out_button, map_zoom_in_button