from dataclasses import dataclass
from typing import List
from src.models.tour import ComputedTour

DELIVERYMAN_SPEED = 15

@dataclass
class DeliveryMan:
    name: str
    availabilities: List[int]
    speed: float
    tourAssigned: ComputedTour
    
    def __init__(self, name: str, speed: float = DELIVERYMAN_SPEED, tourAssigned: ComputedTour = None) -> None:
        self.name = name
        self.speed = speed
        self.tourAssigned = tourAssigned

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        if value:
            self._name = value
        else:
            raise ValueError("Name can't be empty")

    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, value: float) -> None:
        if value >= 0:
            self._speed = value
        else:
            raise ValueError("Speed can't be negative")
        
    @property
    def tourAssigned(self) -> ComputedTour:
        return self.tourAssigned

    @tourAssigned.setter
    def tourAssigned(self, value: ComputedTour) -> None:
        if value:
            self.tourAssigned = value
        else:
            raise ValueError("TourAssigned can't be empty")
