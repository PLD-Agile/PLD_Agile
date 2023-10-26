from dataclasses import dataclass

from src.models.map.intersection import Intersection


@dataclass
class DeliveryLocation:
    origin: Intersection
    destination: Intersection
    positionOnSegment: float
