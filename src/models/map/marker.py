from dataclasses import dataclass

from src.models.map.position import Position


@dataclass
class Marker:
    position: Position
