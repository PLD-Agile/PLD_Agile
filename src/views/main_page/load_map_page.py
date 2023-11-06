from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QLabel, QVBoxLayout

from src.controllers.navigator.page import Page
from src.services.map import MapLoaderService
from src.views.modules.main_page_navigator.navigator import \
    get_main_page_navigator
from src.views.modules.main_page_navigator.routes import \
    MainPageNavigationRoutes
from src.views.ui.button import Button
from src.views.ui.button_group import ButtonGroup

DEFAULT_BUTTONS = [
    ("small", "src/assets/smallMap.xml"),
    ("medium", "src/assets/mediumMap.xml"),
    ("large", "src/assets/largeMap.xml"),
]


class LoadMapPage(Page):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        load_map_button = Button("Load map")
        load_map_button.clicked.connect(self.ask_user_for_map)

        default_buttons = []

        for name, path in DEFAULT_BUTTONS:
            button = Button(name)
            button.clicked.connect(lambda _, path=path: self.load_map(path))
            default_buttons.append(button)

        load_map_default_button_group = ButtonGroup(default_buttons)

        layout.addWidget(QLabel("Load from file:"))
        layout.addWidget(load_map_button)
        layout.addWidget(QLabel("Load from default maps:"))
        layout.addWidget(load_map_default_button_group)

        self.setLayout(layout)

    def ask_user_for_map(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Choose map", "${HOME}", "XML files (*.xml)"
        )
        if file_name:
            self.load_map(file_name)

    def load_map(self, path: str) -> None:
        MapLoaderService.instance().load_map_from_xml(path)
        get_main_page_navigator().replace(MainPageNavigationRoutes.DELIVERY_FORM)
