from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

from src.views.layout import Header
from views.modules.app_navigation import app_navigation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(600, 400)

        self.setWindowTitle("My App")

        widget = QWidget()
        layout = QVBoxLayout()

        header = Header()
        router_outlet = app_navigation.get_router_outlet()

        widget.setLayout(layout)
        layout.addWidget(header)
        layout.addWidget(router_outlet)

        # Set the central widget of the Window.
        self.setCentralWidget(widget)
