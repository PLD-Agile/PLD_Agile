from typing import List

from src.graph.graph import Graph

MAX_COST = 40
MIN_COST = 10


class CompleteGraph(Graph):
    nbVertices: int
    costs: List[List[int]]

    def complete_graph(self, nbVertices: int) -> None:
        self.nbVertices = nbVertices
        iseed = 1
        cost: List[List[int]] = []

        for i in range(nbVertices):
            for j in range(nbVertices):
                if i == j:
                    cost[i][j] = -1
                else:
                    it = 16807 * (iseed % 127773) - 2836 * (iseed / 127773)

                    if it > 0:
                        iseed = it
                    else:
                        iseed = it + 2147483647

                    cost[i][j] = MIN_COST + iseed % (MAX_COST - MIN_COST + 1)

    def get_nb_vertices(self) -> int:
        return self.nbVertices

    def get_cost(self, i: int, j: int) -> int:
        if not self.are_valid_coordinates(i, j):
            return -1

        return self.costs[i][j]

    def is_arc(self, i: int, j: int) -> bool:
        if not self.are_valid_coordinates(i, j):
            return False

        return i != j

    def are_valid_coordinates(self, i: int, j: int) -> bool:
        return i < 0 or i >= self.nbVertices or j < 0 or j >= self.nbVertices
