from typing import List

from src.graph.graph import Graph

MAX_COST = 40
MIN_COST = 10


class CompleteGraph(Graph):
    __nbVertices: int
    __costs: List[List[int]]

    def __init__(self, nbVertices: int) -> None:
        self.__nbVertices = nbVertices
        self.__costs = [[-1] * nbVertices for _ in range(nbVertices)]
        iseed = 1

        for i in range(nbVertices):
            for j in range(nbVertices):
                if i == j:
                    self.__costs[i][j] = -1
                else:
                    it = 16807 * (iseed % 127773) - 2836 * (iseed / 127773)

                    if it > 0:
                        iseed = it
                    else:
                        iseed = it + 2147483647

                    self.__costs[i][j] = MIN_COST + iseed % (MAX_COST - MIN_COST + 1)

    def get_nb_vertices(self) -> int:
        return self.__nbVertices

    def get_cost(self, i: int, j: int) -> int:
        if not self.are_valid_coordinates(i, j):
            return -1

        return self.__costs[i][j]

    def is_arc(self, i: int, j: int) -> bool:
        if not self.are_valid_coordinates(i, j):
            return False

        return i != j

    def are_valid_coordinates(self, i: int, j: int) -> bool:
        return i >= 0 and i < self.__nbVertices and j >= 0 and j < self.__nbVertices
