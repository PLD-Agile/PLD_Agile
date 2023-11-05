from dataclasses import dataclass
from typing import List
#from src.models.tour import ComputedTour

DELIVERYMAN_SPEED = 15

@dataclass
class DeliveryMan:
    name: str
    availabilities: List[int]
    speed: float = DELIVERYMAN_SPEED
    #tourAssigned: ComputedTour

    @property
    def name(self) -> str:
        """Get the value of the name of the delivery man."""
        return self.name

    @name.setter
    def name(self, value: str) -> None:
        """Set the value of the name of the delivery man."""
        self.name = value
        
    @property
    def availabilities(self) -> List[int]:
        """Get the value of the availabilities hours of the delivery man."""
        return self.availabilities
    
    @availabilities.setter
    def availabilities(self, value: List[int]) -> None:
        """Set the value of the availabilities hours of the delivery man."""
        self.availabilities = value
    
    def __sortByHour(self, hour):
        """ Returns the value in format 24 hours """
        return hour % 24

    def addAvailableHour(self, value: int) -> None:
        """Add an hour to the availabilities hours of the delivery man."""
        self.availabilities.append(value)
        self.availabilities = sorted(self.availabilities, key=self.__sortByHour)
    
    def removeAvailableHour(self, value: int) -> None:
        """ Removes the first aparition of an hour from the availabilities hours of the de livery man. """
        if value in self.availabilities:
            self.availabilities.remove(value)

    @property
    def speed(self) -> float:
        """Get the value of the speed of the delivery man."""
        return self.speed

    @speed.setter
    def speed(self, value: float) -> None:
        """Set the value of the speed of the delivery man."""
        self.speed = value
        
    """ 
    ---------
    DEPRECATED
    ----------
    @property
    def tourAssigned(self) -> ComputedTour:
        return self.tourAssigned

    @tourAssigned.setter
    def tourAssigned(self, value: ComputedTour) -> None:
        if value:
            self.tourAssigned = value
        else:
            raise ValueError("TourAssigned can't be empty") """
