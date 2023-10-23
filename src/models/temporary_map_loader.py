"""THIS IS ONLY FOR DEVELOPMENT, A BETTER MAP LOADER NEEDS TO BE IMPLEMENTED LATER
"""
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Position:
    latitude: float
    longitude: float


@dataclass
class Intersection(Position):
    id: int


@dataclass
class Segment:
    name: str
    origin: Intersection
    destination: Intersection
    length: float


@dataclass
class Map:
    intersections: Dict[int, Intersection]
    segments: List[Segment]
    max_latitude: float
    min_latitude: float
    max_longitude: float
    min_longitude: float

    def get_size(self) -> float:
        return (self.max_latitude - self.min_latitude) * (
            self.max_longitude - self.min_longitude
        )


class TemporaryMapLoader:
    def load_map(self) -> Map:
        intersections = {}
        segments = []
        max_latitude: float = sys.maxsize * -1
        min_latitude: float = sys.maxsize
        max_longitude: float = sys.maxsize * -1
        min_longitude: float = sys.maxsize

        tree = ET.parse("src/assets/largeMap.xml")

        for el in tree.getroot():
            if el.tag == "intersection":
                intersection = Intersection(
                    id=int(el.attrib["id"]),
                    latitude=float(el.attrib["latitude"]),
                    longitude=float(el.attrib["longitude"]),
                )

                if intersection.latitude > max_latitude:
                    max_latitude = intersection.latitude
                if intersection.latitude < min_latitude:
                    min_latitude = intersection.latitude
                if intersection.longitude > max_longitude:
                    max_longitude = intersection.longitude
                if intersection.longitude < min_longitude:
                    min_longitude = intersection.longitude

                intersections[intersection.id] = intersection
            elif el.tag == "segment":
                segment = Segment(
                    name=el.attrib["name"],
                    origin=intersections[int(el.attrib["origin"])],
                    destination=intersections[int(el.attrib["destination"])],
                    length=float(el.attrib["length"]),
                )
                segments.append(segment)

        return Map(
            intersections,
            segments,
            max_latitude,
            min_latitude,
            max_longitude,
            min_longitude,
        )


if __name__ == "__main__":
    loader = TemporaryMapLoader()
    print(loader.load_map())
