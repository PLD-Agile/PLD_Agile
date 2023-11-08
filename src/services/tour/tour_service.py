from typing import List, Optional, Tuple

from reactivex import Observable, combine_latest
from reactivex.operators import map
from reactivex.subject import BehaviorSubject

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.map import Position
from src.models.tour import ComputedTour, DeliveryLocation, DeliveryRequest, TourRequest
from src.services.map.delivery_location_service import DeliveryLocationService
from src.services.map.map_service import MapService
from src.services.singleton import Singleton
from src.services.tour.tour_computing_service import TourComputingService
from src.services.tour.tour_saving_service import TourSavingService

COLORS = ["#3875ff", "green", "yellow", "purple", "orange", "pink"]


class TourService(Singleton):
    __tour_requests: BehaviorSubject[List[TourRequest]]
    __computed_tours: BehaviorSubject[List[ComputedTour]]
    __selected_delivery_request: BehaviorSubject[Optional[DeliveryRequest]]

    def __init__(self) -> None:
        self.__tour_requests = BehaviorSubject([])
        self.__computed_tours = BehaviorSubject([])
        self.__selected_delivery_request = BehaviorSubject(None)

    @property
    def tour_requests(self) -> Observable[List[TourRequest]]:
        return self.__tour_requests

    @property
    def tour_requests_delivery_locations(
        self,
    ) -> Observable[Tuple[DeliveryLocation, List[DeliveryLocation]]]:
        return combine_latest(
            self.__selected_delivery_request,
            self.__tour_requests,
        ).pipe(
            map(
                lambda x: (
                    x[0],
                    [
                        delivery_request.location
                        for tour_request in x[1]
                        for delivery_request in tour_request.deliveries
                    ],
                )
            )
        )

    @property
    def computed_tours(self) -> Observable[List[ComputedTour]]:
        return self.__computed_tours

    def clear(self) -> None:
        self.__tour_requests.on_next([])
        self.__computed_tours.on_next([])

    def get_tour_requests(self) -> List[TourRequest]:
        return self.__tour_requests.value

    def get_tour_request_for_delivery_man(
        self, delivery_man: DeliveryMan
    ) -> Optional[TourRequest]:
        return next(
            (
                tour
                for tour in self.__tour_requests.value
                if tour.delivery_man == delivery_man
            ),
            None,
        )

    def get_computed_tours(self) -> List[ComputedTour]:
        return self.__computed_tours.value

    def select_delivery_request(
        self, delivery_request: Optional[DeliveryRequest]
    ) -> None:
        self.__selected_delivery_request.on_next(delivery_request)

    def add_delivery_request(
        self, position: Position, delivery_man: DeliveryMan, time_window: int
    ) -> DeliveryRequest:
        """Add a delivery request to the tour requests and publish the update.

        Args:
            position (Position): Approximate position of the delivery
            delivery_man (DeliveryMan): Delivery Man to assign the delivery to
            timeWindow (int): Time window for the delivery
        """
        # tour_request = self.__tour_requests.value.get(delivery_man, None)
        tour_request = self.get_tour_request_for_delivery_man(delivery_man)

        if not tour_request:
            tour_request = TourRequest(
                deliveries=[],
                delivery_man=delivery_man,
            )
            self.__tour_requests.value.append(tour_request)
            
        delivery_request = DeliveryRequest(
                location=DeliveryLocationService.instance().find_delivery_location_from_position(
                    position
                ),
                timeWindow=time_window,
            )

        tour_request.deliveries.append(delivery_request)

        self.__tour_requests.on_next(self.__tour_requests.value)

        # TODO: review how to compute tours when adding a delivery request
        self.compute_tours()
        
        return delivery_request

    def remove_delivery_request(
        self, delivery_request: DeliveryRequest, delivery_man: DeliveryMan
    ) -> None:
        """Remove a delivery request from the tour requests and publish the update.

        Args:
            delivery_request (DeliveryRequest): Delivery request to remove
            delivery_man (DeliveryMan): Delivery Man to remove the delivery from
        """
        tour_request = self.get_tour_request_for_delivery_man(delivery_man)

        if not tour_request:
            return

        tour_request.deliveries.remove(delivery_request)

        self.__tour_requests.on_next(self.__tour_requests.value)

        if self.__selected_delivery_request.value == delivery_request:
            self.__selected_delivery_request.on_next(None)

        # TODO: review how to compute tours when adding a delivery request
        self.compute_tours()

    def clear_tour_requests(self) -> None:
        self.__tour_requests.on_next({})

    def compute_tours(self) -> None:
        """Compute the tours and publish the update."""
        # TODO: Use service to get computed tours
        # Example:

        computed_tours: List[ComputedTour] = []
        map = MapService.instance().get_map()

        tours_intersection_ids = TourComputingService.instance().compute_tours(
            tour_requests=self.__tour_requests.value,
            map=map,
        )
        for index, tour_intersection_ids in enumerate(tours_intersection_ids):
            if not self.__tour_requests.value[index].deliveries:
                continue

            computed_tours.append(
                ComputedTour(
                    deliveries=self.__tour_requests.value[index].deliveries,
                    delivery_man=DeliveryMan("Bill", [8, 9, 10]),
                    route=[
                        map.segments[origin_id][destination_id]
                        for origin_id, destination_id in zip(
                            tour_intersection_ids, tour_intersection_ids[1:]
                        )
                    ],
                    length=0,
                    color=COLORS[index % len(COLORS)],
                )
            )
        self.__computed_tours.on_next(computed_tours)

    def clear_computed_tours(self) -> None:
        """Clear the computed tours and publish the update."""
        self.__computed_tours.on_next([])

    def save_tours(self, path: str) -> None:
        """Save the computed tours to a file.

        Args:
            path (str): Path to the file
        """
        TourSavingService.instance().save_tours(self.__computed_tours.value, path)

    def load_tours(self, path: str) -> None:
        """Load the computed tours from a file.

        Args:
            path (str): Path to the file
        """
        self.__computed_tours.on_next(TourSavingService.instance().load_tours(path))
