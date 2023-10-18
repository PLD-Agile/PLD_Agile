from collections.abc import Iterator
from typing import List
from graph.graph import Graph
from src.tsp.template_tsp import TemplateTSP
from src.tsp.seq_iter import SeqIter

class TSP1(TemplateTSP):
    def bound(self, current_vertex: int, unvisited: List[int]) -> int:
        return 0
    
    def iterator(self, current_vertex: int, unvisited: List[int], graph: Graph) -> Iterator[int]:
        return SeqIter(unvisited, current_vertex, graph)