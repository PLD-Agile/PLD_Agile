from src.models.map import Map
from src.models.tour import ComputedTour, DeliveryRequest, TourRequest
from src.services.singleton import Singleton
from src.services.tour.tour_service import TourService
import networkx as nx
import xml.etree.ElementTree as ET
import random


class TourComputingService(Singleton):
    # def compute_tours(self, tour_requests, map):
    def compute_tours(self):
        xml_file = "C:/Users/hicham/py_workshop/PLD_Agile/src/assets/smallMap.xml"
        mapGraph = self.create_graph_from_xml(xml_file)
        # Generate 5 random delivery locations
        random_locations = self.generate_random_delivery_locations(mapGraph, 5)
        print(random_locations)
        shortest_path_graph = self.compute_shortest_path_graph(mapGraph, random_locations)
        for source, target, data in shortest_path_graph.edges(data=True):
            path = data['path']
            length = data['length']
            print(f"Path from {source} to {target}:")
            print(f"Path: {path}")
            print(f"Length: {length}\n")

    #  Replace this with the data from the Map model
    def create_graph_from_xml(self, xml_file):
        G = nx.DiGraph()  # Directed graph

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Create nodes for intersections
            for intersection_elem in root.findall('intersection'):
                intersection_id = int(intersection_elem.get('id'))
                G.add_node(intersection_id, latitude=float(intersection_elem.get('latitude')),
                           longitude=float(intersection_elem.get('longitude')))

            # Create edges for road segments
            for segment_elem in root.findall('segment'):
                origin_id = int(segment_elem.get('origin'))
                destination_id = int(segment_elem.get('destination'))
                length = float(segment_elem.get('length'))
                G.add_edge(origin_id, destination_id, length=length)

            return G

        except ET.ParseError:
            print("Error parsing XML file.")

    def generate_random_delivery_locations(self, graph, num_locations):
        delivery_locations = []
        nodes = list(graph.nodes())

        for _ in range(num_locations):
            random_node = random.choice(nodes)
            delivery_locations.append(random_node)

        return delivery_locations

    # Calculate the compute_shortest_path_graph for the random locations
    def compute_shortest_path_graph(self, graph, delivery_locations):
        G = nx.DiGraph()

        # Add delivery locations as nodes
        for location in delivery_locations:
            G.add_node(location)

        # Compute shortest path distances and paths between delivery locations
        for source in delivery_locations:
            for target in delivery_locations:
                if source != target:
                    shortest_path_length, shortest_path = nx.single_source_dijkstra(graph, source, target,
                                                                                    weight='length')
                    G.add_edge(source, target, length=shortest_path_length, path=shortest_path)

        return G


tourService = TourComputingService.instance()
tourService.compute_tours()
