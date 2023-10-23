from typing import Optional, List, Tuple

from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import (
    QBrush,
    QMouseEvent,
    QPen,
    QWheelEvent,
    QTransform,
    QColor,
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

from src.models.temporary_map_loader import Map, Position, Segment
from src.views.utils.theme import Theme
from src.views.utils.icon import get_icon_pixmap


AlignBottom = bool


class MapView(QGraphicsView):
    MAX_SCALE = 8
    SCALE_INTENSITY = 3
    DEFAULT_SCALE = 1.25
    MARKER_BASE_SIZE = 0.003
    MARKER_ZOOM_ADJUSTMENT = 0.5
    MARKER_RESOLUTION_RESOLUTION = 250
    SEGMENT_BASE_SIZE = 0.00005
    SEGMENT_ZOOM_ADJUSTMENT = 0.1

    __scene: Optional[QGraphicsScene] = None
    __map: Optional[Map] = None
    __scale_factor: int = 1
    __on_map_click: Subject[Position] = Subject()
    __segments: List[QAbstractGraphicsShapeItem] = []
    __markers: List[Tuple[QAbstractGraphicsShapeItem, AlignBottom]] = []

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.__set_config()

    @property
    def on_map_click(self) -> Observable[Position]:
        return self.__on_map_click

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
            self.__add_segment(segment)

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
        icon_pixmap = get_icon_pixmap(icon, self.MARKER_RESOLUTION_RESOLUTION, color)

        icon_shape = self.__scene.addPixmap(icon_pixmap)
        icon_shape.setPos(
            QPointF(
                # Longitude - half of the icon size (to center it)
                position.longitude - self.MARKER_BASE_SIZE / 2,
                # Latitude - icon size + 1% of the icon size (align it with the bottom of the icon which includes a little margin)
                (
                    position.latitude
                    - self.MARKER_BASE_SIZE
                    + (self.MARKER_BASE_SIZE * 0.01)
                )
                if align_bottom
                else (position.latitude - self.MARKER_BASE_SIZE / 2),
            )
        )
        icon_shape.setScale(self.MARKER_BASE_SIZE / self.MARKER_RESOLUTION_RESOLUTION)

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

        self.__on_map_click.on_next(position)

    def __add_segment(
        self, segment: Segment, color: QColor = Qt.GlobalColor.black
    ) -> None:
        segmentLine = self.__scene.addLine(
            segment.origin.longitude,
            segment.origin.latitude,
            segment.destination.longitude,
            segment.destination.latitude,
            QPen(QBrush(color), self.__get_pen_size()),
        )
        self.__segments.append(segmentLine)

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

        translateX, translateY = (
            origin.x() + self.MARKER_BASE_SIZE / 2,
            (origin.y() + self.MARKER_BASE_SIZE)
            if align_bottom
            else (origin.y() + self.MARKER_BASE_SIZE / 2),
        )
        scale_factor = 1 / (
            self.__scale_factor * self.MARKER_ZOOM_ADJUSTMENT
            + (1 - self.MARKER_ZOOM_ADJUSTMENT)
        )

        marker.setTransform(
            QTransform()
            .translate(translateX, translateY)
            .scale(scale_factor, scale_factor)
            .translate(-translateX, -translateY)
        )

    def __get_pen_size(self, scale: float = 1) -> float:
        return (
            self.SEGMENT_BASE_SIZE
            / (
                self.__scale_factor * self.SEGMENT_ZOOM_ADJUSTMENT
                + (1 - self.SEGMENT_ZOOM_ADJUSTMENT)
            )
            * scale
        )

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
