from dataclasses import dataclass
from typing import Dict, List

from src.models.map.intersection import Intersection
from src.models.map.map_size import MapSize
from src.models.map.segment import Segment


@dataclass
class Map:
    intersections: Dict[int, Intersection]
    segments: List[Segment]
    segments_map: Dict[int, Dict[int, Segment]]
    """2D map of segments, indexed by origin and destination intersection IDs. Ex: segments_map[1][2] gives the segment between intersection 1 and 2."""
    warehouse: Intersection
    size: MapSize
