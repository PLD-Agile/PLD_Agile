from dataclasses import dataclass
from typing import Dict, List

from src.models.map.intersection import Intersection
from src.models.map.map_size import MapSize
from src.models.map.segment import Segment


@dataclass
class Map:
    intersections: Dict[int, Intersection]
    segments: List[Segment]
    warehouse: Intersection
    size: MapSize
