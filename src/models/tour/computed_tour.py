from dataclasses import dataclass
from typing import List

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.map.segment import Segment
from src.models.tour.computed_delivery import ComputedDelivery


@dataclass
class ComputedTour:
    deliveries: List[ComputedDelivery]
    delivery_man: DeliveryMan
    route: List[Segment]
    length: float
    color: str
