from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap
from src.views.utils.theme import Theme


class MapView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        
        QLabel(self).setPixmap(QPixmap('src/assets/map.png').scaled(500, 500))
        
        self.setFixedSize(500, 500)
        Theme.set_background_color(self, "black")