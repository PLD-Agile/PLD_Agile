import itertools
import xml.etree.ElementTree as ET
from typing import List, Tuple

import networkx as nx

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.map import Map, Segment
from src.models.tour import (
    ComputedDelivery,
    ComputedTour,
    DeliveryLocation,
    DeliveryRequest,
    TourRequest,
)
from src.services.singleton import Singleton


class TourComputingService(Singleton):
    def compute_tours(
        self, tour_requests: List[TourRequest], map: Map
    ) -> List[List[int]]:
        """Compute tours for a list of tour requests."""
        map_graph = self.create_graph_from_map(map)
        warehouse = DeliveryRequest(
            DeliveryLocation(Segment("", map.warehouse, map.warehouse, 0), 0), 0
        )

        return [
            self.solve_tsp(
                self.compute_shortest_path_graph(
                    map_graph, [warehouse] + tour_request.deliveries
                )
            )
            for tour_request in tour_requests
        ]

    #  Replace this with the data from the Map model
    def create_graph_from_map(self, map: Map) -> nx.Graph:
        """Create a directed graph from an XML file."""
        graph = nx.DiGraph()

        graph.add_node(map.warehouse.id)

        for intersection in map.intersections.values():
            graph.add_node(
                intersection.id,
                latitude=float(intersection.latitude),
                longitude=float(intersection.longitude),
            )

        for segment in map.get_all_segments():
            graph.add_edge(
                segment.origin.id, segment.destination.id, length=segment.length
            )

        return graph

    def compute_shortest_path_graph(
        self, graph: nx.Graph, deliveries: List[DeliveryRequest]
    ) -> nx.DiGraph:
        """Compute the shortest path graph between delivery locations."""
        G = nx.DiGraph()

        # Add delivery locations as nodes
        for delivery in deliveries:
            G.add_node(delivery.location.segment.origin.id)

        # Compute the shortest path distances and paths between delivery locations
        for source in deliveries:
            for target in deliveries:
                if source != target:
                    try:
                        shortest_path_length, shortest_path = nx.single_source_dijkstra(
                            graph,
                            source.location.segment.origin.id,
                            target.location.segment.origin.id,
                            weight="length",
                        )
                    except nx.NetworkXNoPath:
                        continue
                    G.add_edge(
                        source.location.segment.origin.id,
                        target.location.segment.origin.id,
                        length=shortest_path_length,
                        path=shortest_path,
                    )

        return G

    # TODO : solve the tsp algorithm from the shortest path graph, return the route and the length

    def solve_tsp(self, shortest_path_graph: nx.Graph) -> List[int]:
        shortest_cycle_length = float("inf")
        shortest_cycle = None
        route = []

        # Generate all permutations of delivery points to find the shortest cycle
        delivery_points = list(shortest_path_graph.nodes())
        warehouse_id = delivery_points.pop(0)
        for permuted_points in itertools.permutations(delivery_points):
            is_valid_tuple = True
            permuted_points = list(permuted_points)
            permuted_points = [warehouse_id] + permuted_points
            cycle_length = 0
            for i in range(len(permuted_points) - 1):
                source = permuted_points[i]
                target = permuted_points[i + 1]
                if not shortest_path_graph.has_edge(source,target):
                    is_valid_tuple = False
                    break  
                cycle_length += shortest_path_graph[source][target]["length"]

            if not is_valid_tuple:
                continue
            # Add the length of the last edge back to the starting point to complete the cycle
            if not shortest_path_graph.has_edge(permuted_points[-1],permuted_points[0]):
                continue                                    
            cycle_length += shortest_path_graph[permuted_points[-1]][
                permuted_points[0]
            ]["length"]

            if cycle_length < shortest_cycle_length:
                shortest_cycle_length = cycle_length
                shortest_cycle = permuted_points

        # Compute the actual route from the shortest cycle

        for i in range(len(shortest_cycle) - 1):
            source = shortest_cycle[i]
            target = shortest_cycle[i + 1]
            dijkstra_path = shortest_path_graph[source][target]["path"]
            route = route + dijkstra_path
            route.pop()

        # Complete the route with the path from the last delivery point to the first
        dijkstra_path = shortest_path_graph[shortest_cycle[-1]][shortest_cycle[0]][
            "path"
        ]

        route = route + dijkstra_path

        return route
