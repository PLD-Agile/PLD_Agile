from PyQt6.QtWidgets import (
    QWidget,
    QSizePolicy,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsRectItem,
    QStackedLayout,
    QLabel,
    QFrame
)
from PyQt6.QtGui import QBrush, QPen
from PyQt6.QtCore import Qt
from src.views.utils.theme import Theme
from typing import Optional
from src.models.temporary_map_loader import Map, TemporaryMapLoader


class MapView(QGraphicsView):
    __scene: Optional[QGraphicsScene] = None
    __zoom: int = 0

    def __init__(self) -> None:
        super().__init__()

        self.__set_config()
        
        map_loader = TemporaryMapLoader()
        self.__build_scene(map_loader.load_map())
        
        self.fitMap()
        
    def fitMap(self):
        if self.__scene:
            self.fitInView(self.__scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)

    def __build_scene(self, map: Map):
        self.__scene = QGraphicsScene(
            map.min_longitude,
            map.min_latitude,
            map.max_longitude - map.min_longitude,
            map.max_latitude - map.min_latitude
        )
        self.__scene.setBackgroundBrush(QBrush(Qt.GlobalColor.white))
        self.setScene(self.__scene)
        
        for segment in map.segments:
            self.__scene.addLine(
                segment.origin.longitude,
                segment.origin.latitude,
                segment.destination.longitude,
                segment.destination.latitude,
                QPen(QBrush(Qt.GlobalColor.black), 0.00005)
            )

    def __set_config(self):
        self.setTransformationAnchor(
            QGraphicsView.ViewportAnchor.AnchorUnderMouse
        )
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.setFrameShape(QFrame.Shape.NoFrame)
        Theme.set_background_color(self, "white")