from typing import List, Optional

from reactivex import Observable
from reactivex.subject import BehaviorSubject
from reactivex.operators import map

from src.models.errors.no_value_error import NoValueError
from src.services.singleton import Singleton
from src.services.tour.tour_saving_service import TourSavingService
from src.models.tour import TourRequest, DeliveryRequest, DeliveryLocation, ComputedTour
from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.map import Position, Intersection


class TourService(Singleton):
    __tour_requests: BehaviorSubject[List[TourRequest]]
    __computed_tours: BehaviorSubject[List[ComputedTour]]
    
    def __init__(self) -> None:
        self.__tour_requests = BehaviorSubject([])
        self.__computed_tours = BehaviorSubject([])
    
    
    @property
    def tour_requests(self) -> Observable[List[TourRequest]]:
        return self.__tour_requests
    
    @property
    def tour_requests_delivery_locations(self) -> Observable[List[DeliveryLocation]]:
        return self.__tour_requests.pipe(
            map(lambda tour_requests: [delivery_request.location for tour_request in tour_requests for delivery_request in tour_request.deliveries])
        )
    
    @property
    def computed_tours(self) -> Observable[List[ComputedTour]]:
        return self.__computed_tours
    
    def get_tour_requests(self) -> List[TourRequest]:
        return self.__tour_requests.value
    
    def get_tour_request_for_delivery_man(self, delivery_man: DeliveryMan) -> Optional[DeliveryMan]:
        return next((tour for tour in self.__tour_requests.value if tour.delivery_man == delivery_man), None)
    
    def get_computed_tours(self) -> List[ComputedTour]:
        return self.__computed_tours.value
    
    def add_delivery_request(self, position: Position, delivery_man: DeliveryMan, timeWindow: int) -> None:
        # tour_request = self.__tour_requests.value.get(delivery_man, None)
        tour_request = self.get_tour_request_for_delivery_man(delivery_man)
        
        if not tour_request:
            tour_request = TourRequest(
                deliveries=[],
                delivery_man=delivery_man,
            )
            self.__tour_requests.value.append(tour_request)
        
        tour_request.deliveries.append(
            DeliveryRequest(
                location=DeliveryLocation(
                    # TODO: Use service to find the actual intersection
                    origin=Intersection(
                        id=-1,
                        longitude=position.longitude,
                        latitude=position.latitude,
                    ),
                    destination=None,
                    positionOnSegment=0,
                ),
                timeWindow=timeWindow,
            )
        )
        
        self.__tour_requests.on_next(self.__tour_requests.value)
        
    def remove_delivery_request(self, delivery_request: DeliveryRequest, delivery_man: DeliveryMan) -> None:
        tour_request = self.get_tour_request_for_delivery_man(delivery_man)
        
        if not tour_request:
            return
        
        tour_request.deliveries.remove(delivery_request)
            
        self.__tour_requests.on_next(self.__tour_requests.value)
        
    def clear_tour_requests(self) -> None:
        self.__tour_requests.on_next({})
        
    def compute_tours(self) -> None:
        # TODO: Use service to get computed tours
        # Example:
        # computed_tours = TourComputingService.instance().compute_tours(self.__tour_requests.value)
        
        computed_tours = []
        
        self.__computed_tours.on_next(computed_tours)
        
    def clear_computed_tours(self) -> None:
        self.__computed_tours.on_next([])
    
    def save_tours(self, path: str) -> None:
        TourSavingService.instance().save_tours(self.__computed_tours.value, path)
        
    def load_tours(self, path: str) -> None:
        self.__computed_tours.on_next(TourSavingService.instance().load_tours(path))
