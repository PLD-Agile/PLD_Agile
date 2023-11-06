from dataclasses import dataclass
from typing import Dict, Generator, List

from src.models.map.intersection import Intersection
from src.models.map.map_size import MapSize
from src.models.map.segment import Segment


@dataclass
class Map:
    intersections: Dict[int, Intersection]
    segments: Dict[int, Dict[int, Segment]]
    """2D map of segments, indexed by origin and destination intersection IDs. Ex: segments_map[1][2] gives the segment between intersection 1 and 2."""
    warehouse: Intersection
    size: MapSize

    def get_all_segments(self) -> Generator[Segment, any, None]:
        """Returns all segments in the map."""
        for origin_segments in self.segments.values():
            for segment in origin_segments.values():
                yield segment