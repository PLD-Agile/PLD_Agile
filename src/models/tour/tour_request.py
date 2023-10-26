from dataclasses import dataclass
from typing import List
from src.models.tour.delivery_request import DeliveryRequest
from src.models.delivery_man.delivery_man import DeliveryMan


@dataclass
class TourRequest:
    deliveries: List[DeliveryRequest]
    delivery_man: DeliveryMan