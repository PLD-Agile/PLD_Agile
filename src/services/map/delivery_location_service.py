import sys
from typing import List, Optional

from src.models.map import Intersection, Position, Segment
from src.models.tour import DeliveryLocation
from src.services.map.map_service import MapService
from src.services.singleton import Singleton


class DeliveryLocationService(Singleton):
    def find_delivery_location_from_position(
        self, position: Position
    ) -> DeliveryLocation:
        """Find the delivery location from a position."""

        # TODO: Find the point on the segment
        closest_intersection = self.__find_closest_intersection(position)
        segments = self.__get_intersection_segments(closest_intersection)

        if len(segments) == 0:
            raise Exception("No segments found for intersection")

        return DeliveryLocation(
            segment=segments[0],
            positionOnSegment=0,
        )

    def __find_closest_intersection(self, position: Position) -> Intersection:
        """Find the closest intersection to a position.

        Args:
            position (Position): Position to find the closest intersection to

        Returns:
            Intersection: Closest intersection to the position
        """

        found: Optional[Intersection] = None
        found_distance: float = sys.maxsize

        for intersection in MapService.instance().get_map().intersections.values():
            if intersection.id not in MapService.instance().get_map().segments:
                continue
            
            distance = intersection.distance_to(position)
            if distance < found_distance:
                found = intersection
                found_distance = distance

        return found

    def __get_intersection_segments(self, intersection: Intersection) -> List[Segment]:
        return list(MapService.instance().get_map().segments[intersection.id].values())
