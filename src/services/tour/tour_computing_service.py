import itertools
from typing import List

import networkx as nx

from src.models.map import Map, Segment
from src.models.tour import (
    DeliveriesComputingResult,
    DeliveryLocation,
    DeliveryRequest,
    TourComputingResult,
    TourRequest,
)
from src.services.singleton import Singleton


class TourComputingService(Singleton):
    def compute_tour(self, tour_request: TourRequest, map: Map) -> TourComputingResult:
        """Compute tours for a list of tour requests.

        Args:
            tour_request (TourRequest): Tour request
            map (Map): Map

        Returns:
            TourComputingResult: Result of the computation
        """
        map_graph = self.create_graph_from_map(map)
        warehouse = DeliveryRequest(
            DeliveryLocation(Segment(-1, "", map.warehouse, map.warehouse, 0), 0), 8
        )

        return self.solve_tsp(
            self.compute_shortest_path_graph(
                map_graph, [warehouse] + list(tour_request.deliveries.values())
            )
        )

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
            G.add_node(
                delivery.location.segment.origin.id, timewindow=delivery.time_window
            )

        # Compute the shortest path distances and paths between delivery locations
        for source in deliveries:
            for target in deliveries:
                if source != target:
                    # add time windows constraints
                    if (
                        target.time_window + 1 <= source.time_window
                        and target != deliveries[0]
                    ):
                        continue
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

    def solve_tsp(self, shortest_path_graph: nx.Graph) -> TourComputingResult:
        shortest_cycle_length = float("inf")
        shortest_cycle: List[DeliveriesComputingResult] = []
        route = []

        # Generate all permutations of delivery points to find the shortest cycle
        delivery_points = list(shortest_path_graph.nodes())
        warehouse_id = delivery_points.pop(0)
        for permuted_points in itertools.permutations(delivery_points):
            is_valid_tuple = True
            permuted_points = list(permuted_points)
            permuted_points = [warehouse_id] + permuted_points
            cycle_length = 0
            current_time = 8 * 60  # Starting time at the warehouse (8 a.m.)

            times = []

            for i in range(len(permuted_points) - 1):
                source = permuted_points[i]
                target = permuted_points[i + 1]
                if not shortest_path_graph.has_edge(source, target):
                    is_valid_tuple = False
                    break
                travel_distance = shortest_path_graph[source][target]["length"]
                cycle_length += travel_distance

                # Check if the delivery time is within the time window
                time_window = shortest_path_graph.nodes[target]["timewindow"] * 60
                travel_time = (
                    travel_distance / 15000
                ) * 60  # Convert meters to minutes based on speed (15 km/h)
                arrival_time = current_time + travel_time

                if arrival_time < time_window:
                    # Courier arrives before the time window, wait until it starts
                    current_time = time_window + 5  # Add 5 minutes for delivery
                elif arrival_time <= time_window + 60:
                    # Courier arrives within the time window
                    current_time = arrival_time + 5  # Add 5 minutes for delivery
                else:
                    # Courier arrives after the time window, this tuple is invalid
                    is_valid_tuple = False
                    break

                times.append(current_time)

            if not is_valid_tuple:
                continue
            # Add the length of the last edge back to the starting point to complete the cycle
            if not shortest_path_graph.has_edge(
                permuted_points[-1], permuted_points[0]
            ):
                continue
            cycle_length += shortest_path_graph[permuted_points[-1]][
                permuted_points[0]
            ]["length"]

            if cycle_length < shortest_cycle_length:
                shortest_cycle_length = cycle_length
                shortest_cycle = list(zip(permuted_points, [0] + times))

        # Compute the actual route from the shortest cycle
        if shortest_cycle == []:
            return []

        for i in range(len(shortest_cycle) - 1):
            source, source_time = shortest_cycle[i]
            target, target_time = shortest_cycle[i + 1]
            dijkstra_path = shortest_path_graph[source][target]["path"]
            route = route + dijkstra_path
            route.pop()

        # Complete the route with the path from the last delivery point to the first
        dijkstra_path = shortest_path_graph[shortest_cycle[-1][0]][
            shortest_cycle[0][0]
        ]["path"]

        route = route + dijkstra_path

        return TourComputingResult(
            route=route,
            deliveries=shortest_cycle,
        )
