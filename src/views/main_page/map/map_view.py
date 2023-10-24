from typing import List, Literal, Optional, Tuple

from PyQt6.QtCore import QPointF, QRectF, Qt
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QIcon,
    QMouseEvent,
    QPen,
    QTransform,
    QWheelEvent,
)
from PyQt6.QtWidgets import (
    QAbstractGraphicsShapeItem,
    QFrame,
    QGraphicsScene,
    QGraphicsView,
    QSizePolicy,
    QWidget,
)
from reactivex import Observable
from reactivex.subject import BehaviorSubject, Subject

from src.models.map import Map, Marker, Position, Segment
from src.services.map.map_service import MapService
from src.views.main_page.map.map_marker import AlignBottom, MapMarker
from src.views.utils.icon import get_icon_pixmap
from src.views.utils.theme import Theme


class MapView(QGraphicsView):
    """Widget to display a Map"""

    MAX_SCALE = 8
    """Maximum scale factor for the map (1 = no zoom, 2 = 2x zoom, etc.)
    """
    SCROLL_INTENSITY = 2
    """Intensity of the zoom when scrolling (higher = more zoom)
    """
    DEFAULT_ZOOM_ACTION = 1.25
    """Zoom factor when clicking on the zoom in/out buttons
    """
    MARKER_INITIAL_SIZE = 0.045
    """Marker size when zoom is 1 (1 = marker is same width as the map)
    """
    MARKER_ZOOM_ADJUSTMENT = 0.35
    """Amount of zoom adjustment for the markers (1 = marker stays the same size, 0 = marker scales with the map)
    """
    MARKER_RESOLUTION_RESOLUTION = 250
    """Image resolution of the marker
    """
    SEGMENT_INITIAL_SIZE = 0.00005
    """Size of a segment when zoom is 1
    """
    SEGMENT_ZOOM_ADJUSTMENT = -0.075
    """Amount of zoom adjustment for the segments (1 = segment stays the same size, 0 = segment scales with the map)
    """

    __scene: Optional[QGraphicsScene] = None
    __map: Optional[Map] = None
    __scale_factor: int = 1
    __segments: List[QAbstractGraphicsShapeItem] = []
    __markers: List[MapMarker] = []
    __route_markers: List[MapMarker] = []
    __marker_size: Optional[int] = None
    __ready: BehaviorSubject[bool] = BehaviorSubject(False)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.__set_config()

        MapService.instance().map.subscribe(
            lambda map: self.set_map(map) if map else self.reset()
        )
        MapService.instance().markers().subscribe(self.__on_markers_change)

    @property
    def ready(self) -> Observable[bool]:
        """Subject that emit a boolean when the map is ready to be used"""
        return self.__ready

    def set_map(self, map: Map):
        """Set the map and initialize the view

        Arguments:
            map (Map): Map to display
        """
        scene_rect = QRectF(
            map.size.min.longitude,
            map.size.min.latitude,
            map.size.width,
            map.size.height,
        )

        if self.__scene:
            self.reset()
            self.__scene.setSceneRect(scene_rect)
        else:
            self.__scene = QGraphicsScene(scene_rect)

        self.__map = map

        self.__scene.setBackgroundBrush(QBrush(Qt.GlobalColor.white))
        self.setScene(self.__scene)

        for segment in map.segments:
            self.__add_segment(segment)

        self.__marker_size = self.__scene.sceneRect().width() * self.MARKER_INITIAL_SIZE

        self.add_marker(
            position=map.warehouse,
            icon="warehouse",
            color=QColor("#1e8239"),
            align_bottom=False,
            scale=0.5,
        )

        self.fit_map()

        self.__ready.on_next(True)

    def fit_map(self):
        """Adjust the view to fit the all map"""
        if self.__scene:
            self.fitInView(self.__scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
            self.__scale_factor = 1
            self.__scale_map(1)

    def add_marker(
        self,
        position: Position,
        icon: QIcon | str = "map-marker-alt",
        color: QColor = QColor("#f54242"),
        align_bottom: AlignBottom = True,
        scale: float = 1,
    ) -> MapMarker:
        """Add a marker on the map at a given position

        Args:
            position (Position): Position of the marker
            icon (str, optional): Icon to display. Defaults to "map-marker-alt".
            color (QColor, optional): Color of the icon. Defaults to QColor("#f54242").
            align_bottom (AlignBottom, optional): Whether the icon should be aligned at the bottom (ex: for map pin). Set to false if is a normal icon like a X. Defaults to True.
        """
        marker_size = self.__marker_size * scale

        icon_pixmap = get_icon_pixmap(icon, self.MARKER_RESOLUTION_RESOLUTION, color)
        icon_position = self.__get_marker_position(position, marker_size, align_bottom)

        icon_shape = self.__scene.addPixmap(icon_pixmap)
        icon_shape.setPos(icon_position)
        icon_shape.setScale(marker_size / self.MARKER_RESOLUTION_RESOLUTION)

        marker = MapMarker(icon_shape, align_bottom, scale)

        self.__adjust_marker(marker)

        self.__markers.append(marker)

        return marker

    def zoom_in(self):
        """Zoom in the map"""
        self.__scale_map(self.DEFAULT_ZOOM_ACTION)

    def zoom_out(self):
        """Zoom out the map"""
        self.__scale_map(1 / self.DEFAULT_ZOOM_ACTION)

    def reset(self):
        """Reset the map to its initial state"""
        self.__ready.on_next(False)
        if self.__scene:
            self.__scene.clear()
        self.__segments = []
        self.__markers = []
        self.__route_markers = []
        self.__scale_factor = 1
        self.__marker_size = None
        self.__map = None

    def wheelEvent(self, event: QWheelEvent) -> None:
        """Method called when the user scrolls on the map

        Zoom the map in/out depending on the scroll direction
        """
        if self.__scene and event.angleDelta().y() != 0:
            self.__scale_map(
                1
                + (self.__map.size.area * self.SCROLL_INTENSITY)
                * event.angleDelta().y()
            )

    def mouseDoubleClickEvent(self, event: QMouseEvent | None) -> None:
        """Method called when the user double clicks on the map

        Send the position of the click to the on_map_click subject
        """
        if not self.__scene:
            return

        position = self.mapToScene(event.pos())
        position = Position(position.x(), position.y())

        MapService.instance().add_marker(Marker(position))

    def __on_markers_change(self, markers: List[Marker]) -> None:
        for marker in self.__route_markers:
            self.__scene.removeItem(marker.shape)

        self.__route_markers = []

        for marker in markers:
            map_marker = self.add_marker(marker.position)
            self.__route_markers.append(map_marker)

    def __add_segment(
        self, segment: Segment, color: QColor = QColor("#9c9c9c")
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
            QPen(
                QBrush(color),
                self.__get_pen_size(),
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
            ),
        )
        self.__segments.append(segmentLine)

    def __scale_map(self, factor: float):
        """Scales the map for a given factor. This is used to zoom in and out.

        Args:
            factor (float): Scale factor
        """
        if not self.__scene:
            return

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
        """Adjust map segments and markers to the current map scale"""
        for segment in self.__segments:
            pen = segment.pen()
            pen.setWidthF(self.__get_pen_size())
            segment.setPen(pen)

        for marker in self.__markers:
            self.__adjust_marker(marker)

    def __adjust_marker(self, marker: MapMarker) -> None:
        """Adjust a marker to the current map scale

        Args:
            marker (QAbstractGraphicsShapeItem): Marker to adjust
            align_bottom (AlignBottom):  Whether the icon should be aligned at the bottom (ex: for map pin). Set to false if is a normal icon like a X. Defaults to True.
        """
        origin = marker.shape.transformOriginPoint()

        marker_size = self.__marker_size * marker.scale

        translate = self.__get_marker_position(
            origin, marker_size, marker.align_bottom, direction=-1
        )
        scale_factor = 1 / (
            self.__scale_factor * self.MARKER_ZOOM_ADJUSTMENT
            + (1 - self.MARKER_ZOOM_ADJUSTMENT)
        )

        marker.shape.setTransform(
            QTransform()
            .translate(translate.x(), translate.y())
            .scale(scale_factor, scale_factor)
            .translate(-translate.x(), -translate.y())
        )

    def __get_marker_position(
        self,
        position: QPointF | Position,
        marker_size: float,
        align_bottom: bool,
        direction: Literal[1, -1] = 1,
    ) -> QPointF:
        x = position.x() if isinstance(position, QPointF) else position.x
        y = position.y() if isinstance(position, QPointF) else position.y

        return QPointF(
            x - (marker_size / 2 * direction),
            (y - (marker_size - (marker_size * 0.01)) * direction)
            if align_bottom
            else (y - (marker_size / 2 * direction)),
        )

    def __get_pen_size(self, scale: float = 1) -> float:
        """Calculate the pen size for a given scale

        Args:
            scale (float, optional): Additional scale. Useful to make some segment bigger than others. Defaults to 1.

        Returns:
            float: Pen size
        """
        return (
            self.SEGMENT_INITIAL_SIZE
            / (
                self.__scale_factor * self.SEGMENT_ZOOM_ADJUSTMENT
                + (1 - self.SEGMENT_ZOOM_ADJUSTMENT)
            )
            * scale
        )

    def __set_config(self):
        """Initiate config for the view."""
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
