from PyQt6.QtWidgets import QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from src.services.map.map_service import MapService

from src.controllers.navigator.page import Page
from src.views.modules.main_page_navigator.navigator import get_main_page_navigator
from src.views.modules.main_page_navigator.routes import MainPageNavigationRoutes
from src.views.ui.button import Button

class CurrentTourPage(Page):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        exit_map_button = Button("Exit map")
        exit_map_button.clicked.connect(self.exit_map)

        layout.addWidget(QLabel("CurrentTourPage works!"))
        layout.addWidget(exit_map_button)

        self.setLayout(layout)
        
    def exit_map(self):
        MapService.instance().set_map(None)
        get_main_page_navigator().replace(MainPageNavigationRoutes.LOAD_MAP)
