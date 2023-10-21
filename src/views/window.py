from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget

from src.views.layout import Header
from src.views.modules.main_navigation import main_navigation


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(600, 400)

        self.setWindowTitle("My App")

        widget = QWidget()
        layout = QVBoxLayout()

        header = Header()
        router_outlet = main_navigation.get_router_outlet()

        widget.setLayout(layout)
        layout.addWidget(header)
        layout.addWidget(router_outlet)

        # Set the central widget of the Window.
        self.setCentralWidget(widget)
