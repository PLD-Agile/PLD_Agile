from PyQt6.QtWidgets import QGridLayout, QMainWindow, QPushButton, QVBoxLayout, QWidget

from src.views.layout import Header
from src.views.utils.theme import Color, Theme
from views.modules.app_navigation import app_navigation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(1000, 630)
        self.setContentsMargins(0, 0, 0, 0)

        self.setWindowTitle("My App")

        self.setCentralWidget(self.build_central_widget())

        Theme.set_background_color(self, Color.BACKGROUND)

    def build_central_widget(self) -> QWidget:
        widget = QWidget()
        layout = QGridLayout()

        layout.setContentsMargins(0, 0, 0, 0)

        header = Header()
        router_outlet = app_navigation.get_router_outlet()

        widget.setLayout(layout)
        layout.addWidget(header, 0, 0)
        layout.addWidget(router_outlet, 1, 0)

        layout.setRowStretch(0, 0)
        layout.setRowStretch(1, 1)

        return widget
