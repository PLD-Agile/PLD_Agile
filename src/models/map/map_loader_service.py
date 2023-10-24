import xml.etree.ElementTree as ET
from typing import Dict, List
from xml.etree.ElementTree import Element

from src.models.map.intersection import Intersection
from src.models.map.map import Map
from src.models.map.map_size import MapSize
from src.models.map.position import Position
from src.models.map.segment import Segment
from src.models.singleton import Singleton


class MapLoaderService(Singleton):
    def load_map_from_xml(self, path: str) -> Map:
        """Loads an XML file and create a Map instance from it.

        Args:
            path (str): Path to the XML file to import (relative to the project root)

        Returns:
            Map: Map instance
        """
        return self.create_map_from_xml(ET.parse(path).getroot())

    def create_map_from_xml(self, element: Element) -> Map:
        """Creates a Map instance from an XML element.

        Args:
            element (Element): XML element

        Returns:
            Map: Map instance
        """
        intersections: Dict[int, Intersection] = {}
        segments: List[Segment] = []
        map_size = MapSize.inverse_max_size()

        for el in element:
            if el.tag == "intersection":
                intersection = Intersection.from_element(el)
                intersections[intersection.id] = intersection
                self.__update_map_size(map_size, intersection)
            elif el.tag == "segment":
                segments.append(Segment.from_element(el, intersections))

        return Map(intersections, segments, map_size)

    def __update_map_size(self, map_size: MapSize, position: Position) -> None:
        map_size.max = Position.max(map_size.max, position)
        map_size.min = Position.min(map_size.min, position)
