import xml.etree.ElementTree as ET
from typing import List, Tuple

import networkx as nx

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.map import Map, Segment
from src.models.tour import ComputedDelivery, ComputedTour, DeliveryRequest, TourRequest
from src.services.singleton import Singleton


class TourComputingService(Singleton):
    def compute_tours(
        self, tour_requests: List[TourRequest], map: Map
    ) -> List[ComputedTour]:
        """Compute tours for a list of tour requests."""
        map_graph = self.create_graph_from_xml(map)

        computed_tours: List[ComputedTour] = []

        for tour_request in tour_requests:
            route, length = self.solve_tsp(map_graph, map, tour_request.deliveries)

            computed_tours.append(
                ComputedTour(
                    deliveries=[
                        ComputedDelivery(
                            location=delivery.location,
                            time=0,
                        )
                        for delivery in tour_request.deliveries
                    ],
                    delivery_man=DeliveryMan(
                        name="John Doe",
                        availabilities=[],
                    ),
                    route=route,
                    length=length,
                    color="green",
                )
            )

        print(computed_tours)

        return computed_tours

    #  Replace this with the data from the Map model
    def create_graph_from_xml(self, map: Map) -> nx.Graph:
        """Create a directed graph from an XML file."""
        graph = nx.DiGraph()

        graph.add_node(map.warehouse.id)

        for intersection in map.intersections.values():
            graph.add_node(
                intersection.id,
                latitude=float(intersection.latitude),
                longitude=float(intersection.longitude),
            )

        for segment in map.segments:
            graph.add_edge(
                segment.origin.id, segment.destination.id, length=segment.length
            )

        return graph

    def compute_shortest_path_graph(
        self, graph: nx.Graph, delivery_locations
    ) -> nx.DiGraph:
        """Compute the shortest path graph between delivery locations."""
        G = nx.DiGraph()

        # Add delivery locations as nodes
        for location in delivery_locations:
            G.add_node(location)

        # Compute the shortest path distances and paths between delivery locations
        for source in delivery_locations:
            for target in delivery_locations:
                if source != target:
                    try:
                        shortest_path_length, shortest_path = nx.single_source_dijkstra(
                            graph, source, target, weight="length"
                        )
                    except nx.NetworkXNoPath:
                        continue
                    G.add_edge(
                        source, target, length=shortest_path_length, path=shortest_path
                    )

        return G

    # TODO : solve the tsp algorithm from the shortest path graph, return the route and the length

    def solve_tsp(
        self, shortest_path_graph: nx.Graph, map: Map, deliveries: List[DeliveryRequest]
    ) -> Tuple[List[Segment], float]:
        cycle: List[Segment] = []
        cycle_length = 0
        
        warehouse_route_intersections_ids = nx.shortest_path(shortest_path_graph, map.warehouse.id, deliveries[0].location.segment.origin.id, weight="length")
        
        for cycle_origin_id, cycle_destination_id in zip(
            warehouse_route_intersections_ids, warehouse_route_intersections_ids[1:]
        ):
            length = shortest_path_graph[cycle_origin_id][cycle_destination_id][
                "length"
            ]
            cycle_length += length
            cycle.append(map.segments_map[cycle_origin_id][cycle_destination_id])

        # Loops through the deliveries in pairs ([1, 2], [2, 3], [3, 4], ...])
        for delivery_origin, delivery_destination in zip(deliveries, deliveries[1:]):
            # Returns a list of the intersections IDs to go through to go from the origin to the destination
            delivery_intersections_ids = nx.shortest_path(
                shortest_path_graph,
                delivery_origin.location.segment.origin.id,
                delivery_destination.location.segment.origin.id,
                weight="length",
            )

            # Loops through the intersections IDs in pairs ([1, 2], [2, 3], [3, 4], ...)
            for cycle_origin_id, cycle_destination_id in zip(
                delivery_intersections_ids, delivery_intersections_ids[1:]
            ):
                length = shortest_path_graph[cycle_origin_id][cycle_destination_id][
                    "length"
                ]
                cycle_length += length
                cycle.append(map.segments_map[cycle_origin_id][cycle_destination_id])
                
        
        # Returns to the warehouse
        warehouse_route_intersections_ids = nx.shortest_path(shortest_path_graph, deliveries[-1].location.segment.origin.id, map.warehouse.id, weight="length")
        
        for cycle_origin_id, cycle_destination_id in zip(
            warehouse_route_intersections_ids, warehouse_route_intersections_ids[1:]
        ):
            length = shortest_path_graph[cycle_origin_id][cycle_destination_id][
                "length"
            ]
            cycle_length += length
            cycle.append(map.segments_map[cycle_origin_id][cycle_destination_id])

        return cycle, cycle_length
