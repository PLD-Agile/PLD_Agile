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
from PyQt6.QtWidgets import QFrame, QGraphicsScene, QGraphicsView, QSizePolicy, QWidget
from reactivex import Observable
from reactivex.subject import BehaviorSubject
from services.command.commands.add_delivery_request_command import AddDeliveryRequestCommand
from src.services.command.command_service import CommandService

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.map import Map, Position, Segment
from src.models.tour import ComputedTour, DeliveryLocation
from src.services.map.map_service import MapService
from src.services.tour.tour_service import TourService
from src.views.main_page.map.map_annotation import MapAnnotation
from src.views.main_page.map.map_annotation_collection import (
    MapAnnotationCollection,
    MarkersTypes,
    SegmentTypes,
)
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
    __marker_size: Optional[int] = None
    __map_annotations: MapAnnotationCollection = MapAnnotationCollection()
    __ready: BehaviorSubject[bool] = BehaviorSubject(False)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.__set_config()

        MapService.instance().map.subscribe(
            lambda map: self.set_map(map) if map else self.reset()
        )
        TourService.instance().tour_requests_delivery_locations.subscribe(
            self.__on_update_delivery_locations
        )
        TourService.instance().computed_tours.subscribe(self.__on_update_computed_tours)

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

        for segment in map.get_all_segments():
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
        marker_type: MarkersTypes = MarkersTypes.Default,
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

        self.__map_annotations.markers.append(marker_type, marker)

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
        self.__scale_factor = 1
        self.__marker_size = None
        self.__map_annotations.clear_all()
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

        CommandService.instance().execute(AddDeliveryRequestCommand(
            position=position,
            delivery_man=DeliveryMan("John Doe", []),
            time_window=8,
        ))

    def __on_update_delivery_locations(
        self,
        deliveries: Tuple[Optional[DeliveryLocation], List[DeliveryLocation]],
    ):
        selected_delivery_location, delivery_locations = deliveries

        for marker in self.__map_annotations.markers.get(MarkersTypes.Delivery):
            self.__scene.removeItem(marker.shape)

        self.__map_annotations.markers.clear(MarkersTypes.Delivery)

        for delivery_location in delivery_locations:
            self.__map_annotations.markers.append(
                MarkersTypes.Delivery,
                self.add_marker(
                    position=delivery_location.segment.origin,
                    icon="map-marker-alt",
                    color=QColor("#f54242"),
                    scale=1.5 if delivery_location == selected_delivery_location else 1,
                ),
            )

    def __on_update_computed_tours(self, computed_tours: List[ComputedTour]):
        for maker in self.__map_annotations.segments.get(SegmentTypes.Tour):
            self.__scene.removeItem(maker.shape)

        self.__map_annotations.segments.clear(SegmentTypes.Tour)

        for computed_tour in computed_tours:
            for segment in computed_tour.route:
                self.__add_segment(
                    segment=segment,
                    color=QColor(computed_tour.color),
                    scale=2,
                    segment_type=SegmentTypes.Tour,
                )

    def __add_segment(
        self,
        segment: Segment,
        color: QColor = QColor("#9c9c9c"),
        scale: float = 1,
        segment_type: SegmentTypes = SegmentTypes.Default,
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
                self.__get_pen_size() * scale,
                Qt.PenStyle.SolidLine,
                Qt.PenCapStyle.RoundCap,
            ),
        )

        self.__map_annotations.segments.append(
            segment_type, MapAnnotation(segmentLine, scale)
        )

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
        for segment in self.__map_annotations.segments.get_all():
            pen = segment.shape.pen()
            pen.setWidthF(self.__get_pen_size() * segment.scale)
            segment.shape.setPen(pen)

        for marker in self.__map_annotations.markers.get_all():
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
