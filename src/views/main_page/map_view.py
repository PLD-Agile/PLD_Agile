from typing import Optional, List, Tuple

from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import (
    QBrush,
    QMouseEvent,
    QPen,
    QWheelEvent,
    QTransform,
    QColor,
    QIcon,
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
    """Widget to display a Map
    """
    
    MAX_SCALE = 8
    """Maximum scale factor for the map (1 = no zoom, 2 = 2x zoom, etc.)
    """
    SCROLL_INTENSITY = 3
    """Intensity of the zoom when scrolling (higher = more zoom)
    """
    DEFAULT_ZOOM_ACTION = 1.25
    """Zoom factor when clicking on the zoom in/out buttons
    """
    MARKER_BASE_SIZE = 0.003
    """Size of a marker when zoom is 1
    """
    MARKER_ZOOM_ADJUSTMENT = 1
    """Amount of zoom adjustment for the markers (1 = marker stays the same size, 0 = marker scales with the map)
    """
    MARKER_RESOLUTION_RESOLUTION = 250
    """Image resolution of the marker
    """
    SEGMENT_BASE_SIZE = 0.00005
    """Size of a segment when zoom is 1
    """
    SEGMENT_ZOOM_ADJUSTMENT = 0.1
    """Amount of zoom adjustment for the segments (1 = segment stays the same size, 0 = segment scales with the map)
    """

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
        """Subject that emit the position on the map when a user double clicks on it
        """
        return self.__on_map_click

    def set_map(self, map: Map):
        """Set the map and initialize the view
        
        Arguments:
            map (Map): Map to display
        """
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
        """Adjust the view to fit the all map
        """
        if self.__scene:
            self.fitInView(self.__scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.__scale_factor = 1

    def add_marker(
        self,
        position: Position,
        icon: QIcon | str = "map-marker-alt",
        color: QColor = QColor("#f54242"),
        align_bottom: AlignBottom = True,
    ):
        """Add a marker on the map at a given position

        Args:
            position (Position): Position of the marker
            icon (str, optional): Icon to display. Defaults to "map-marker-alt".
            color (QColor, optional): Color of the icon. Defaults to QColor("#f54242").
            align_bottom (AlignBottom, optional): Whether the icon should be aligned at the bottom (ex: for map pin). Set to false if is a normal icon like a X. Defaults to True.
        """
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
        """Zoom in the map
        """
        self.__scale_map(self.DEFAULT_ZOOM_ACTION)

    def zoom_out(self):
        """Zoom out the map
        """
        self.__scale_map(1 / self.DEFAULT_ZOOM_ACTION)

    def wheelEvent(self, event: QWheelEvent) -> None:
        """Method called when the user scrolls on the map
        
        Zoom the map in/out depending on the scroll direction
        """
        if self.__scene and event.angleDelta().y() != 0:
            self.__scale_map(
                1
                + (self.__map.get_size() * self.SCROLL_INTENSITY)
                * event.angleDelta().y()
            )

    def mouseDoubleClickEvent(self, event: QMouseEvent | None) -> None:
        """Method called when the user double clicks on the map

        Send the position of the click to the on_map_click subject
        """
        position = self.mapToScene(event.pos())
        position = Position(position.x(), position.y())

        self.add_marker(position)

        self.__on_map_click.on_next(position)

    def __add_segment(
        self, segment: Segment, color: QColor = Qt.GlobalColor.black
    ) -> None:
        """Add a segment on the map

        Args:
            segment (Segment): Segment
            color (QColor, optional): Color. Defaults to Qt.GlobalColor.black.
        """
        segmentLine = self.__scene.addLine(
            segment.origin.longitude,
            segment.origin.latitude,
            segment.destination.longitude,
            segment.destination.latitude,
            QPen(QBrush(color), self.__get_pen_size()),
        )
        self.__segments.append(segmentLine)

    def __scale_map(self, factor: float):
        """Scales the map for a given factor. This is used to zoom in and out.

        Args:
            factor (float): Scale factor
        """
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
        """Adjust map segments and markers to the current map scale
        """
        for segment in self.__segments:
            segment.setPen(QPen(QBrush(Qt.GlobalColor.black), self.__get_pen_size()))

        for marker, align_bottom in self.__markers:
            self.__adjust_marker(marker, align_bottom)

    def __adjust_marker(
        self, marker: QAbstractGraphicsShapeItem, align_bottom: AlignBottom
    ) -> None:
        """Adjust a marker to the current map scale

        Args:
            marker (QAbstractGraphicsShapeItem): Marker to adjust
            align_bottom (AlignBottom):  Whether the icon should be aligned at the bottom (ex: for map pin). Set to false if is a normal icon like a X. Defaults to True.
        """
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
        """Calculate the pen size for a given scale

        Args:
            scale (float, optional): Additional scale. Useful to make some segment bigger than others. Defaults to 1.

        Returns:
            float: Pen size
        """
        return (
            self.SEGMENT_BASE_SIZE
            / (
                self.__scale_factor * self.SEGMENT_ZOOM_ADJUSTMENT
                + (1 - self.SEGMENT_ZOOM_ADJUSTMENT)
            )
            * scale
        )

    def __set_config(self):
        """Initiate config for the view.
        """
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
