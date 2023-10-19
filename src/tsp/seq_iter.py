from collections.abc import Iterator
from typing import List

from src.graph.graph import Graph


class SeqIter(Iterator[int]):
    """Iterates over unvisited vertex in graph (excluding current vertex)"""

    __candidates: List[int]

    def __init__(self, unvisited: List[int], current_vertex: int, graph: Graph):
        self.__candidates = []

        for s in unvisited:
            if graph.is_arc(current_vertex, s):
                self.__candidates.append(s)

    def __iter__(self) -> Iterator[int]:
        return self

    def __next__(self) -> int:
        try:
            return self.__candidates.pop()
        except IndexError:
            raise StopIteration
