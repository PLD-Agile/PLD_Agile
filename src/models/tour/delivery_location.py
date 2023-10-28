from dataclasses import dataclass

from src.models.map.segment import Segment


@dataclass
class DeliveryLocation:
    segment: Segment
    positionOnSegment: float
