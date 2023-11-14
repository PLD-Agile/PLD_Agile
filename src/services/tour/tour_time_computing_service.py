import math
from datetime import datetime, timedelta
from typing import Dict, List

from src.config import Config
from src.models.map import Segment
from src.models.tour import ComputedDelivery, ComputedTour, DeliveryRequest, TourRequest
from src.services.map.map_service import MapService
from src.services.singleton import Singleton


class TourTimeComputingService(Singleton):
    def get_computed_tour_from_route_ids(
        self, tour_request: TourRequest, route: List[int]
    ) -> List[ComputedTour]:
        """Create a computed tour from a request and a computed list of route IDs.

        Args:
            tour_request (TourRequest): Tour request
            routes (List[int]): Computed route

        Returns:
            List[ComputedTour]: Computed tour
        """
        map = MapService.instance().get_map()

        segment_route = [
            map.segments[origin_id][destination_id]
            for origin_id, destination_id in zip(route, route[1:])
        ]

        return ComputedTour.create_from_request(
            tour_request=tour_request,
            deliveries={delivery.id: delivery for delivery in self.__compute_time_for_deliveries(tour_request, segment_route)},
            route=segment_route,
        )

    def __compute_time_for_deliveries(
        self, tour_request: TourRequest, route: List[Segment]
    ) -> List[ComputedDelivery]:
        travel_time = Config.INITIAL_DEPART_TIME

        delivery_requests: Dict[int, DeliveryRequest] = {}
        computed_deliveries: List[ComputedDelivery] = []

        for delivery in tour_request.deliveries.values():
            delivery_requests[delivery.location.segment.origin.id] = delivery

        for segment in route:
            travel_time += self.__calculate_travel_time_for_segment(segment)

            if segment.origin.id in delivery_requests:
                delivery = delivery_requests[segment.origin.id]
                time_window_start = datetime(
                    year=1, month=1, day=1, hour=delivery.time_window
                )

                # Wait until the delivery time window
                if travel_time < time_window_start:
                    travel_time = time_window_start

                if travel_time > time_window_start + Config.TIME_WINDOW_SIZE:
                    raise Exception("Delivery time window exceeded")

                computed_deliveries.append(
                    ComputedDelivery.create_from_request(
                        delivery_request=delivery, time=travel_time
                    )
                )

                # Delivery takes 5 minutes
                travel_time += Config.DELIVERY_TIME

        if len(computed_deliveries) != len(tour_request.deliveries):
            raise Exception(
                "The number of computed deliveries and deliveries must be the same"
            )

        return computed_deliveries

    def __calculate_travel_time_for_segment(self, segment: Segment) -> timedelta:
        return timedelta(
            seconds=math.floor(segment.length / (Config.TRAVELING_SPEED / 3.6))
        )
