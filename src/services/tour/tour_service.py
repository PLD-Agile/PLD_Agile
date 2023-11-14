from typing import Dict, List, Optional, Tuple
from uuid import UUID

from reactivex import Observable, combine_latest
from reactivex.operators import map
from reactivex.subject import BehaviorSubject

from src.models.map import Position
from src.models.tour import (
    ComputedTour,
    DeliveryID,
    DeliveryLocation,
    DeliveryRequest,
    Tour,
    TourID,
    TourRequest,
    Delivery
)
from src.services.delivery_man.delivery_man_service import DeliveryManService
from src.services.map.delivery_location_service import DeliveryLocationService
from src.services.map.map_service import MapService
from src.services.singleton import Singleton
from src.services.tour.tour_computing_service import TourComputingService
from src.services.tour.tour_saving_service import TourSavingService
from src.services.tour.tour_time_computing_service import TourTimeComputingService

COLORS = ["#6929c4", "#1192e8", "#005d5d", "#9f1853", "#198038", "#012749", "#b28600"]


class TourService(Singleton):
    __tour_requests: BehaviorSubject[Dict[TourID, TourRequest]]
    __computed_tours: BehaviorSubject[Dict[TourID, ComputedTour]]
    __selected_delivery: BehaviorSubject[Optional[Delivery]]

    def __init__(self) -> None:
        self.__tour_requests = BehaviorSubject({})
        self.__computed_tours = BehaviorSubject({})
        self.__selected_delivery = BehaviorSubject(None)

        self.__tour_requests.subscribe(lambda _: self.compute_tours())

    @property
    def tour_requests(self) -> Observable[Dict[TourID, TourRequest]]:
        return self.__tour_requests

    @property
    def tour_requests_delivery_locations(
        self,
    ) -> Observable[Tuple[Delivery, List[DeliveryLocation]]]:
        return combine_latest(
            self.__selected_delivery,
            self.__tour_requests,
        ).pipe(
            map(
                lambda x: (
                    x[0],
                    [
                        delivery_request.location
                        for tour_request in x[1].values()
                        for delivery_request in tour_request.deliveries.values()
                    ],
                )
            )
        )

    @property
    def computed_tours(self) -> Observable[Dict[TourID, ComputedTour]]:
        return self.__computed_tours

    @property
    def all_tours(self) -> Observable[List[Tour]]:
        return combine_latest(
            self.__tour_requests,
            self.__computed_tours,
        ).pipe(
            map(
                lambda tours: [
                    (computed_tour if computed_tour else tour_request)
                    for (tour_request, computed_tour) in zip(
                        tours[0].values(), tours[1].values()
                    )
                ]
            )
        )

    def clear(self) -> None:
        self.__tour_requests.on_next({})
        self.__computed_tours.on_next({})

    def get_tour_requests(self) -> List[TourRequest]:
        return self.__tour_requests.value

    def get_computed_tours(self) -> List[ComputedTour]:
        return self.__computed_tours.value

    def select_delivery(
        self, delivery: Optional[Delivery]
    ) -> None:
        self.__selected_delivery.on_next(delivery)

    def add_delivery_request(
        self, position: Position, time_window: int, tour_id: TourID
    ) -> DeliveryRequest:
        """Add a delivery request to the tour requests and publish the update.

        Args:
            position (Position): Approximate position of the delivery
            time_window (int): Time window for the delivery
            tour_id (TourID): ID of the tour to add the delivery to (same as DeliveryMan ID)
        """
        tour_request = self.__get_or_create_tour_request(tour_id)

        delivery_request = DeliveryRequest(
            location=DeliveryLocationService.instance().find_delivery_location_from_position(
                position
            ),
            time_window=time_window,
        )

        tour_request.deliveries[delivery_request.id] = delivery_request

        self.__tour_requests.on_next(self.__tour_requests.value)

        return delivery_request

    def remove_delivery_request(
        self, delivery_request_id: DeliveryID, tour_id: Optional[TourID] = None
    ) -> None:
        """Remove a delivery request from the tour requests and publish the update.

        Args:
            delivery_request_id(DeliverID): ID of the delivery request to remove
            tour_id (TourID): ID of the tour to add the delivery to (same as DeliveryMan ID)
        """
        tour_request = (
            self.__tour_requests.value[tour_id]
            if tour_id
            else next(
                tour_request
                for tour_request in self.__tour_requests.value.values()
                if delivery_request_id in tour_request.deliveries
            )
        )
        delivery_request = tour_request.deliveries[delivery_request_id]

        del tour_request.deliveries[delivery_request_id]

        self.__tour_requests.on_next(self.__tour_requests.value)

        if self.__selected_delivery.value == tour_request:
            self.__selected_delivery.on_next(None)

        return delivery_request

    def update_delivery_request_time_window(
        self, delivery_request_id: DeliveryID, tour_id: TourID, time_window: int
    ) -> int:
        tour_request = self.__tour_requests.value[tour_id]
        delivery_request = tour_request.deliveries[delivery_request_id]

        if delivery_request.time_window == time_window:
            return

        previous_time_window = delivery_request.time_window
        delivery_request.time_window = time_window

        self.__tour_requests.on_next(self.__tour_requests.value)

        return previous_time_window

    def update_delivery_request_delivery_man(
        self, delivery_request_id: DeliveryID, tour_id: TourID, delivery_man_id: UUID
    ) -> UUID:
        if tour_id == delivery_man_id:
            return

        tour_request = self.__tour_requests.value[tour_id]
        delivery_request = tour_request.deliveries[delivery_request_id]

        previous_delivery_man_id = tour_request.delivery_man.id

        del tour_request.deliveries[delivery_request_id]

        self.__get_or_create_tour_request(delivery_man_id).deliveries[
            delivery_request_id
        ] = delivery_request

        self.__tour_requests.on_next(self.__tour_requests.value)

        return previous_delivery_man_id

    def compute_tours(self) -> None:
        """Compute the tours and publish the update."""
        if len(self.__tour_requests.value) == 0:
            self.__computed_tours.on_next({})
            return

        map = MapService.instance().get_map()

        tours_intersection_ids = {
            id: TourComputingService.instance().compute_tour(tour_request, map)
            for (id, tour_request) in self.__tour_requests.value.items()
        }

        computed_tours = {
            id: TourTimeComputingService.instance().get_computed_tour_from_route_ids(
                self.__tour_requests.value[id], tour_intersection_ids
            )
            if tour_intersection_ids
            else None
            for (id, tour_intersection_ids) in tours_intersection_ids.items()
        }

        self.__computed_tours.on_next(computed_tours)

    def clear_tour_requests(self) -> None:
        self.__tour_requests.on_next({})

    def clear_computed_tours(self) -> None:
        """Clear the computed tours and publish the update."""
        self.__computed_tours.on_next({})

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

    def __get_or_create_tour_request(self, tour_id: TourID) -> Tour:
        tour_request = self.__tour_requests.value.get(tour_id)

        if not tour_request:
            tour_request = TourRequest(
                id=tour_id,
                deliveries={},
                delivery_man=DeliveryManService.instance().get_delivery_man(tour_id),
                color=COLORS[len(self.__tour_requests.value) % len(COLORS)],
            )
            self.__tour_requests.value[tour_request.id] = tour_request

        return tour_request
