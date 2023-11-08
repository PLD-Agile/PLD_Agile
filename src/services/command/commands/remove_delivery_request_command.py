from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.tour import DeliveryRequest
from src.services.tour.tour_service import TourService
from src.services.command.abstract_command import AbstractCommand


class RemoveDeliveryRequestCommand(AbstractCommand):
    __delivery_request: DeliveryRequest
    __delivery_man: DeliveryMan
    
    def __init__(self, delivery_request: DeliveryRequest, delivery_man: DeliveryMan) -> None:
        super().__init__('Retrait d\'une demande de livraison')
        self.__delivery_request = delivery_request
        self.__delivery_man = delivery_man
    
    def execute(self) -> None:
        TourService.instance().remove_delivery_request(self.__delivery_request, self.__delivery_man)
        
    def undo(self) -> None:
        TourService.instance().add_delivery_request(
            position=self.__delivery_request.location.segment.origin,
            delivery_man=self.__delivery_man,
            time_window=self.__delivery_request.timeWindow,
        )