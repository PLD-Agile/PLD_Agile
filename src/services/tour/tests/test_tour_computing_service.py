import networkx as nx
from pytest import fixture

from src.services.tour.tour_computing_service import TourComputingService


@fixture
def tour_service():
    return TourComputingService.instance()


def test_compute_tours(tour_service):
    # tour_service.compute_tours()
    pass


def test_compute_shortest_path_graph(tour_service):
    # Create a simple graph for testing
    G = nx.DiGraph()
    G.add_node(1, latitude=0.0, longitude=0.0)
    G.add_node(2, latitude=1.0, longitude=1.0)
    G.add_node(3, latitude=2.0, longitude=2.0)
    G.add_node(4, latitude=3.0, longitude=3.0)
    G.add_edge(1, 2, length=1.0)
    G.add_edge(1, 3, length=2.0)
    G.add_edge(2, 3, length=1.5)
    G.add_edge(3, 4, length=2.5)

    # Define a set of delivery locations
    delivery_locations = [1, 2, 4]

    # Compute the shortest path graph
    shortest_path_graph = tour_service.compute_shortest_path_graph(
        G, delivery_locations
    )

    # Check if the resulting graph is a valid NetworkX DiGraph
    assert isinstance(shortest_path_graph, nx.DiGraph)

    # Check if the edges and path data are correctly calculated
    assert shortest_path_graph[1][2]["length"] == 1.0
    assert shortest_path_graph[1][4]["length"] == 4.5
    assert shortest_path_graph[2][4]["length"] == 4

    assert shortest_path_graph[1][2]["path"] == [1, 2]
    assert shortest_path_graph[1][4]["path"] == [1, 3, 4]
    assert shortest_path_graph[2][4]["path"] == [2, 3, 4]
