from dataclasses import dataclass
from src.models.tour.computed_delivery import ComputedDelivery
from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.map.segment import Segment
from typing import List


@dataclass
class ComputedTour:
    deliveries: List[ComputedDelivery]
    delivery_man: DeliveryMan
    route: List[Segment]
    color: str