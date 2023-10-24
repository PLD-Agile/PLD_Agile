from PyQt6.QtWidgets import QVBoxLayout, QLabel, QFileDialog

from src.controllers.navigator.page import Page
from src.views.ui.button import Button
from src.views.ui.button_group import ButtonGroup
from src.services.map import MapLoaderService


class LoadMapPage(Page):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        
        load_map_button = Button("Load map")
        load_map_button.clicked.connect(self.load_map)
        
        load_map_default_small_button = Button("Default small map")
        load_map_default_small_button.clicked.connect(lambda: MapLoaderService.instance().load_map_from_xml("src/assets/smallMap.xml"))
        load_map_default_medium_button = Button("Default medium map")
        load_map_default_medium_button.clicked.connect(lambda: MapLoaderService.instance().load_map_from_xml("src/assets/mediumMap.xml"))
        load_map_default_large_button = Button("Default large map")
        load_map_default_large_button.clicked.connect(lambda: MapLoaderService.instance().load_map_from_xml("src/assets/largeMap.xml"))
        
        load_map_default_button_group = ButtonGroup([load_map_default_small_button, load_map_default_medium_button, load_map_default_large_button])

        layout.addWidget(QLabel("LoadMapPage works!"))
        layout.addWidget(load_map_button)
        layout.addWidget(load_map_default_button_group)
        
        self.setLayout(layout)

    def load_map(self) -> None:
        file_name, file_type = QFileDialog.getOpenFileName(self, 'Choose map', "${HOME}", "XML files (*.xml)")
        MapLoaderService.instance().load_map_from_xml(file_name)