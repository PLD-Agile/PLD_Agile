import xml.etree.ElementTree as ET
from typing import List

import networkx as nx

from src.models.map import Segment
from src.models.tour import ComputedTour, DeliveryRequest, TourRequest
from src.services.singleton import Singleton


class TourComputingService(Singleton):
    def compute_tours(
        self, tour_requests: List[TourRequest], xml_file
    ) -> List[ComputedTour]:
        """Compute tours for a list of tour requests."""
        map_graph = self.create_graph_from_xml(xml_file)
        computed_tours = []
        for tour_request in tour_requests:
            computed_tour = ComputedTour()
            shortest_path_graph = self.compute_shortest_path_graph(
                map_graph, tour_request.deliveries
            )
            computed_tour.route, computed_tour.length = self.solve_tsp(
                shortest_path_graph
            )
            # TODO: Add color, delivery man, etc.
            computed_tours.append(computed_tour)
        return computed_tours

    #  Replace this with the data from the Map model
    def create_graph_from_xml(self, xml_file) -> nx.DiGraph:
        """Create a directed graph from an XML file."""
        G = nx.DiGraph()  # Directed graph

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Create node for warehouse
            warehouse_id = int(root.find("warehouse").get("address"))
            G.add_node(warehouse_id)

            # Create nodes for intersections
            for intersection_elem in root.findall("intersection"):
                intersection_id = int(intersection_elem.get("id"))
                G.add_node(
                    intersection_id,
                    latitude=float(intersection_elem.get("latitude")),
                    longitude=float(intersection_elem.get("longitude")),
                )

            # Create edges for road segments
            for segment_elem in root.findall("segment"):
                origin_id = int(segment_elem.get("origin"))
                destination_id = int(segment_elem.get("destination"))
                length = float(segment_elem.get("length"))
                G.add_edge(origin_id, destination_id, length=length)

            return G

        except ET.ParseError:
            print("Error parsing XML file.")

    def compute_shortest_path_graph(self, graph, delivery_locations) -> nx.DiGraph:
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

    def solve_tsp(self, shortest_path_graph) -> (List[Segment], float):
        shortest_cycle_length = float("inf")
        shortest_cycle = None
        # Solve the TSP...
        return shortest_cycle, shortest_cycle_length
