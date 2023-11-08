from typing import Optional
from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.map.position import Position
from src.models.tour.delivery_request import DeliveryRequest
from src.services.tour.tour_service import TourService
from src.services.command.abstract_command import AbstractCommand


class AddDeliveryRequestCommand(AbstractCommand):
    __position: Position
    __delivery_man: DeliveryMan
    __time_window: int
    __delivery_request: Optional[DeliveryRequest] = None
    
    def __init__(self, position: Position, delivery_man: DeliveryMan, time_window: int) -> None:
        super().__init__('Ajout d\'une demande de livraison')
        self.__position = position
        self.__delivery_man = delivery_man
        self.__time_window = time_window
        
    def execute(self) -> None:
        self.__delivery_request = TourService.instance().add_delivery_request(
            position=self.__position,
            delivery_man=self.__delivery_man,
            time_window=self.__time_window
        )
    
    def undo(self) -> None:
        if not self.__delivery_request:
            raise Exception('Cannot undo a command that has not been executed')
        
        TourService.instance().remove_delivery_request(self.__delivery_request, self.__delivery_man)
        self.__delivery_request = None