from dataclasses import dataclass

from src.models.tour.delivery_location import DeliveryLocation


@dataclass
class ComputedDelivery:
    location: DeliveryLocation
    time: float
