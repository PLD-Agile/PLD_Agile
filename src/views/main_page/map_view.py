from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QBrush, QMouseEvent, QPen, QWheelEvent
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsScene,
    QGraphicsView,
    QSizePolicy,
)
from reactivex import Observable, Subject

from src.models.temporary_map_loader import Map, Position, TemporaryMapLoader
from src.views.utils.theme import Theme


class MapView(QGraphicsView):
    __scene: Optional[QGraphicsScene] = None
    __map: Optional[Map] = None
    __zoom: int = 0
    __point_added: Subject[Position] = Subject()

    def __init__(self) -> None:
        super().__init__()

        self.__set_config()

        map_loader = TemporaryMapLoader()
        self.__build_scene(map_loader.load_map())

        self.fitMap()

    @property
    def point_added(self) -> Observable[Position]:
        return self.__point_added

    def fitMap(self):
        if self.__scene:
            self.fitInView(
                self.__scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatioByExpanding
            )
            self.__zoom = 0

    def __build_scene(self, map: Map):
        self.__map = map
        self.__scene = QGraphicsScene(
            map.min_longitude,
            map.min_latitude,
            map.max_longitude - map.min_longitude,
            map.max_latitude - map.min_latitude,
        )
        self.__scene.setBackgroundBrush(QBrush(Qt.GlobalColor.white))
        self.setScene(self.__scene)

        for segment in map.segments:
            self.__scene.addLine(
                segment.origin.longitude,
                segment.origin.latitude,
                segment.destination.longitude,
                segment.destination.latitude,
                QPen(QBrush(Qt.GlobalColor.black), 0.00005),
            )

    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.__scene:
            if event.angleDelta().y() > 0:
                factor = 1 + (self.__map.get_size() * 5)
                self.__zoom += 1
            else:
                factor = 1 - (self.__map.get_size() * 5)
                self.__zoom -= 1

            if self.__zoom > 0:
                self.scale(factor, factor)
            elif self.__zoom == 0:
                self.fitMap()
            else:
                self.__zoom = 0

    def mouseDoubleClickEvent(self, event: QMouseEvent | None) -> None:
        position = self.mapToScene(event.pos())

        size = 0.0008

        self.__scene.addEllipse(
            position.x() - size / 2,
            position.y() - size / 2,
            size,
            size,
            Qt.GlobalColor.red,
            Qt.GlobalColor.red,
        )

        self.__point_added.on_next(Position(position.x(), position.y()))

    def __set_config(self):
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setSizePolicy(
            QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        )
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setCursor(Qt.CursorShape.CrossCursor)

        Theme.set_background_color(self, "white")
