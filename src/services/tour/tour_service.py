from typing import Dict, List, Optional, Tuple
from uuid import UUID

from reactivex import Observable, combine_latest
from reactivex.operators import map
from reactivex.subject import BehaviorSubject

from src.models.map import Position
from src.models.tour import (
    ComputedDelivery,
    ComputedTour,
    Delivery,
    DeliveryID,
    DeliveryLocation,
    DeliveryRequest,
    NonComputedTour,
    Tour,
    TourComputingResult,
    TourID,
    TourRequest,
)
from src.services.delivery_man.delivery_man_service import DeliveryManService
from src.services.map.delivery_location_service import DeliveryLocationService
from src.services.map.map_service import MapService
from src.services.singleton import Singleton
from src.services.tour.tour_computing_service import TourComputingService
from src.services.tour.tour_saving_service import TourSavingService
from src.services.tour.tour_time_computing_service import TourTimeComputingService

COLORS = [
    "#598BB4",
    "#E1BC6C",
    "#D5745A",
    "#89BA9C",
    "#9573C1",
    "#7FBBDB",
    "#757592",
    "#A77E56",
    "#A49F9C",
    "#B7D273",
    "#935772",
    "#D17775",
]


class TourService(Singleton):
    __tour_requests: BehaviorSubject[Dict[TourID, TourRequest]]
    __computed_tours: BehaviorSubject[Dict[TourID, Tour]]
    __selected_delivery: BehaviorSubject[Optional[Delivery]]

    def __init__(self) -> None:
        self.__tour_requests = BehaviorSubject({})
        self.__computed_tours = BehaviorSubject({})
        self.__selected_delivery = BehaviorSubject(None)

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
    def computed_tours(self) -> Observable[Dict[TourID, Tour]]:
        return self.__computed_tours

    def clear(self) -> None:
        self.__tour_requests.on_next({})
        self.__computed_tours.on_next({})

    def get_tour_requests(self) -> List[TourRequest]:
        return self.__tour_requests.value

    def get_computed_tours(self) -> List[ComputedTour]:
        return self.__computed_tours.value

    def select_delivery(self, delivery: Optional[Delivery]) -> None:
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

        self.compute_tours()

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

        # if len(tour_request.deliveries) == 0:
        #     del self.__tour_requests.value[tour_request.id]

        self.__tour_requests.on_next(self.__tour_requests.value)

        if self.__selected_delivery.value == tour_request:
            self.__selected_delivery.on_next(None)

        self.compute_tours()

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

        self.compute_tours()

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

        # if len(tour_request.deliveries) == 0:
        #     del self.__tour_requests.value[tour_request.id]

        self.__tour_requests.on_next(self.__tour_requests.value)

        self.compute_tours()

        return previous_delivery_man_id

    def compute_tours(self) -> None:
        """Compute the tours and publish the update."""
        if len(self.__tour_requests.value) == 0:
            self.__computed_tours.on_next({})
            return

        map = MapService.instance().get_map()

        tours_intersection_ids: Dict[TourID, TourComputingResult] = {}

        for id, tour_request in self.__tour_requests.value.items():
            try:
                if len(tour_request.deliveries) > 0:
                    tours_intersection_ids[
                        id
                    ] = TourComputingService.instance().compute_tour(tour_request, map)
            except Exception as e:
                tours_intersection_ids[id] = []

        computed_tours: Dict[TourID, Tour] = {}

        for id, tour_intersection_ids in tours_intersection_ids.items():
            if tour_intersection_ids:
                try:
                    computed_tours[
                        id
                    ] = TourTimeComputingService.instance().get_computed_tour_from_route_ids(
                        self.__tour_requests.value[id], tour_intersection_ids
                    )
                except Exception as e:
                    computed_tours[id] = NonComputedTour.create_from_request(
                        self.__tour_requests.value[id],
                        [f"Erreur lors du calcul du temps de parcours : {str(e)}"],
                    )
            else:
                computed_tours[id] = NonComputedTour.create_from_request(
                    self.__tour_requests.value[id], ["Impossible de trouver un chemin."]
                )

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
        loaded_tours = TourSavingService.instance().load_tours(path)

        for tour in loaded_tours.values():
            updated_deliveries = {}

            for delivery in tour.deliveries.values():
                updated_delivery = ComputedDelivery(
                    location=DeliveryLocation(
                        segment=MapService.instance()
                        .get_map()
                        .segments[delivery.location.segment.origin.id][
                            delivery.location.segment.destination.id
                        ],
                        positionOnSegment=0,
                    ),
                    time=delivery.time,
                )
                updated_deliveries[updated_delivery.id] = updated_delivery

            tour.deliveries = updated_deliveries

        self.__tour_requests.on_next({})
        self.__computed_tours.on_next({})

        DeliveryManService.instance().overwrite(
            {tour.delivery_man.id: tour.delivery_man for tour in loaded_tours.values()}
        )

        self.__tour_requests.on_next(
            {
                id: TourRequest.create_from_computed(tour)
                for id, tour in loaded_tours.items()
            }
        )
        self.__computed_tours.on_next(loaded_tours)

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
