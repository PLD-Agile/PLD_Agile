import xml.etree.ElementTree as ET
from typing import Dict, List
from xml.etree.ElementTree import Element

from src.models.map.intersection import Intersection
from src.models.map.map import Map
from src.models.map.map_size import MapSize
from src.models.map.position import Position
from src.models.map.segment import Segment
from src.services.singleton import Singleton
from src.services.map.map_service import MapService
from src.models.map.errors import MapLoadingError


class MapLoaderService(Singleton):
    def load_map_from_xml(self, path: str) -> Map:
        """Loads an XML file, create a Map instance from it and pass it to the MapService.

        Args:
            path (str): Path to the XML file to import (relative to the project root)

        Returns:
            Map: Map instance
        """
        return self.create_map_from_xml(ET.parse(path).getroot())

    def create_map_from_xml(self, root_element: Element) -> Map:
        """Creates a Map instance from an XML element and pass it to the MapService.

        Args:
            root_element (Element): Root element of the XML

        Returns:
            Map: Map instance
        """
        intersections: Dict[int, Intersection] = {}
        segments: List[Segment] = []
        map_size = MapSize.inverse_max_size()
        warehouse: Intersection = None

        for element in root_element.findall("intersection"):
            intersection = Intersection.from_element(element)
            intersections[intersection.id] = intersection
            self.__update_map_size(map_size, intersection)

        for element in root_element.findall("segment"):
            segments.append(Segment.from_element(element, intersections))

        for element in root_element.findall("warehouse"):
            warehouse = intersections[int(element.attrib["address"])]

        if not warehouse:
            raise MapLoadingError("No warehouse found in the XML file")
        
        map = Map(intersections, segments, warehouse, map_size)
        
        MapService.instance().set_map(map)

        return map

    def __update_map_size(self, map_size: MapSize, position: Position) -> None:
        map_size.max = Position.max(map_size.max, position)
        map_size.min = Position.min(map_size.min, position)
