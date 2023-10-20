import pytest

from src.models.graph.complete_graph import CompleteGraph

NB_VERTICES = 5


class TestCompleteGraph:
    graph: CompleteGraph

    @pytest.fixture(autouse=True)
    def graph(self):
        self.graph = CompleteGraph(NB_VERTICES)

    def test_should_create(self):
        assert self.graph

    def test_should_get_nb_vertices(self):
        assert NB_VERTICES == self.graph.get_nb_vertices()

    def test_should_cost_in_diagonal_be_minus_one(self):
        for i in range(NB_VERTICES):
            assert self.graph.get_cost(i, i) == -1

    def test_should_check_valid_coordinates_with_min(self):
        assert self.graph.are_valid_coordinates(0, 0)

    def test_should_check_valid_coordinates_with_max(self):
        assert self.graph.are_valid_coordinates(NB_VERTICES - 1, NB_VERTICES - 1)

    def test_should_check_invalid_coordinates_with_negative(self):
        assert not self.graph.are_valid_coordinates(-1, -1)

    def test_should_check_invalid_coordinates_with_too_big(self):
        assert not self.graph.are_valid_coordinates(NB_VERTICES, NB_VERTICES)
