from typing import Optional, List, Literal, Tuple
from PyQt6 import QtGui

from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import (
    QBrush,
    QMouseEvent,
    QPen,
    QWheelEvent,
    QTransform,
    QResizeEvent,
    QPainter,
    QColor,
    QPixmap,
)
from PyQt6.QtWidgets import (
    QFrame,
    QGraphicsScene,
    QGraphicsView,
    QSizePolicy,
    QAbstractGraphicsShapeItem,
    QWidget,
)
from reactivex import Observable, Subject
import qtawesome as qta

from src.models.temporary_map_loader import Map, Position, TemporaryMapLoader
from src.views.utils.theme import Theme


AlignBottom = bool


class MapView(QGraphicsView):
    MAX_SCALE = 8
    SCALE_INTENSITY = 3
    DEFAULT_SCALE = 1.25
    ICON_SIZE = 0.003
    ICON_RESOLUTION = 250

    __scene: Optional[QGraphicsScene] = None
    __map: Optional[Map] = None
    __scale_factor: int = 1
    __on_click: Subject[Position] = Subject()
    __segments: List[QAbstractGraphicsShapeItem] = []
    __markers: List[Tuple[QAbstractGraphicsShapeItem, AlignBottom]] = []

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.__set_config()

        map_loader = TemporaryMapLoader()
        self.set_map(map_loader.load_map())

    @property
    def on_click(self) -> Observable[Position]:
        return self.__on_click

    def set_map(self, map: Map):
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
            segmentLine = self.__scene.addLine(
                segment.origin.longitude,
                segment.origin.latitude,
                segment.destination.longitude,
                segment.destination.latitude,
                QPen(QBrush(Qt.GlobalColor.black), self.__get_pen_size()),
            )
            self.__segments.append(segmentLine)

        self.fit_map()

    def fit_map(self):
        if self.__scene:
            self.fitInView(self.__scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.__scale_factor = 1

    def add_marker(
        self,
        position: Position,
        icon: str = "map-marker-alt",
        color: QColor = QColor("#f54242"),
        align_bottom: AlignBottom = True,
    ):
        icon_pixmap = qta.icon(f"fa5s.{icon}").pixmap(
            self.ICON_RESOLUTION, self.ICON_RESOLUTION
        )
        mask = icon_pixmap.createMaskFromColor(
            Qt.GlobalColor.transparent, Qt.MaskMode.MaskInColor
        )
        icon_pixmap.fill(color)
        icon_pixmap.setMask(mask)
        icon_shape = self.__scene.addPixmap(icon_pixmap)
        icon_shape.setPos(
            QPointF(
                # Longitude - half of the icon size (to center it)
                position.longitude - self.ICON_SIZE / 2,
                # Latitude - icon size + 1% of the icon size (align it with the bottom of the icon which includes a little margin)
                (position.latitude - self.ICON_SIZE + (self.ICON_SIZE * 0.01))
                if align_bottom
                else (position.latitude - self.ICON_SIZE / 2),
            )
        )
        icon_shape.setScale(self.ICON_SIZE / self.ICON_RESOLUTION)

        self.__adjust_marker(icon_shape, align_bottom)

        self.__markers.append((icon_shape, align_bottom))

    def zoom_in(self):
        self.__scale_map(self.DEFAULT_SCALE)

    def zoom_out(self):
        self.__scale_map(1 / self.DEFAULT_SCALE)

    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.__scene and event.angleDelta().y() != 0:
            self.__scale_map(
                1
                + (self.__map.get_size() * self.SCALE_INTENSITY)
                * event.angleDelta().y()
            )

    def mouseDoubleClickEvent(self, event: QMouseEvent | None) -> None:
        position = self.mapToScene(event.pos())
        position = Position(position.x(), position.y())

        self.add_marker(position)

        self.__on_click.on_next(position)

    def __scale_map(self, factor: float):
        updated_scale = self.__scale_factor * factor

        if updated_scale < 1:
            self.fit_map()
        else:
            if updated_scale > self.MAX_SCALE:
                factor = self.MAX_SCALE / self.__scale_factor
                updated_scale = self.MAX_SCALE

            self.__scale_factor = updated_scale
            self.scale(factor, factor)

        self.__adjust_map_graphics()

    def __adjust_map_graphics(self) -> None:
        for segment in self.__segments:
            segment.setPen(QPen(QBrush(Qt.GlobalColor.black), self.__get_pen_size()))

        for marker, align_bottom in self.__markers:
            self.__adjust_marker(marker, align_bottom)

    def __adjust_marker(
        self, marker: QAbstractGraphicsShapeItem, align_bottom: AlignBottom
    ) -> None:
        origin = marker.transformOriginPoint()
        scale_ratio = 0.75  # Intensity of the zoom on the marker (bigger means smaller icon on zoom)

        translateX, translateY = (
            origin.x() + self.ICON_SIZE / 2,
            (origin.y() + self.ICON_SIZE)
            if align_bottom
            else (origin.y() + self.ICON_SIZE / 2),
        )
        scale_factor = 1 / self.__scale_factor * scale_ratio + (1 - scale_ratio)

        marker.setTransform(
            QTransform()
            .translate(translateX, translateY)
            .scale(scale_factor, scale_factor)
            .translate(-translateX, -translateY)
        )

    def __get_pen_size(self) -> float:
        return 0.000035 + 0.000025 / self.__scale_factor

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
