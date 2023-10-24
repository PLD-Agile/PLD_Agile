from PyQt6.QtWidgets import QVBoxLayout, QLabel, QFileDialog

from src.controllers.navigator.page import Page
from src.views.ui.button import Button
from src.views.ui.button_group import ButtonGroup
from src.services.map import MapLoaderService

DEFAULT_BUTTONS = [
    ("small", "src/assets/smallMap.xml"),
    ("medium", "src/assets/mediumMap.xml"),
    ("large", "src/assets/largeMap.xml")
]


class LoadMapPage(Page):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        
        load_map_button = Button("Load map")
        load_map_button.clicked.connect(self.load_map)
        
        default_buttons = []
        
        for name, path in DEFAULT_BUTTONS:
            button = Button(name)
            button.clicked.connect(lambda _, path=path: MapLoaderService.instance().load_map_from_xml(path))
            default_buttons.append(button)
        
        load_map_default_button_group = ButtonGroup(default_buttons)

        layout.addWidget(QLabel("LoadMapPage works!"))
        layout.addWidget(load_map_button)
        layout.addWidget(load_map_default_button_group)
        
        self.setLayout(layout)

    def load_map(self) -> None:
        file_name, _ = QFileDialog.getOpenFileName(self, 'Choose map', "${HOME}", "XML files (*.xml)")
        MapLoaderService.instance().load_map_from_xml(file_name)