from dataclasses import dataclass
from typing import Dict
from xml.etree.ElementTree import Element

from src.models.map.intersection import Intersection


@dataclass
class Segment:
    name: str
    origin: Intersection
    destination: Intersection
    length: float

    @staticmethod
    def from_element(
        element: Element, intersections: Dict[int, Intersection]
    ) -> "Segment":
        """Creates a Segment instance from an XML element.

        Args:
            element (Element): XML element
            intersections (Dict[int, Intersection]): Dictionary of intersections

        Returns:
            Segment: Segment instance
        """
        return Segment(
            name=element.attrib["name"],
            origin=intersections[int(element.attrib["origin"])],
            destination=intersections[int(element.attrib["destination"])],
            length=float(element.attrib["length"]),
        )
