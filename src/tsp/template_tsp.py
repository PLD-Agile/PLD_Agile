from src.tsp.tsp import TSP
from typing import List, Optional
from src.graph.graph import Graph
from time import time
import sys
from abc import abstractmethod
from collections.abc import Iterator

class TemplateTSP(TSP):
    __best_sol: List[int]
    __best_sol_cost: int
    __time_limit: int
    __start_time: float
    _graph: Optional[Graph]
    
    def search_solution(self, time_limit: int, graph: Graph) -> None:
        if time_limit <= 0:
            return
        
        self.__best_sol: List[int] = []
        self.__best_sol_cost = sys.maxsize
        self.__time_limit = time_limit
        self.__start_time = time()
        self._graph = graph
        
        unvisited: List[int] = []
        visited: List[int] = []
        
        for i in range(graph.get_nb_vertices()):
            unvisited.append(i)
        
        visited.append(0)
        
        self.branch_and_bound(
            current_vertex=0,
            unvisited=unvisited,
            visited=visited,
            current_cost=0,
        )
    
    def get_solution(self, i: int) -> int:
        if not self._graph or i < 0 or i >= self._graph.get_nb_vertices():
            return -1
        
        return self.__best_sol[i]
    
    def get_solution_cost(self) -> int:
        if not self._graph:
            return -1
        
        return self.__best_sol_cost
        
    def branch_and_bound(self, current_vertex: int, unvisited: List[int], visited: List[int], current_cost: int) -> None:
        if time() - self.__start_time > self.__time_limit:
            return
        
        if not unvisited:
            if self._graph.is_arc(current_vertex, 0):
                if current_cost + self._graph.get_cost(current_vertex, 0) < self.__best_sol_cost:
                    self.__best_sol_cost = current_cost + self._graph.get_cost(current_vertex, 0)
        elif current_cost + self.bound(current_vertex, unvisited) < self.__best_sol_cost:
            it = self.iterator(current_vertex, unvisited, self._graph)
            
            for next_vertex in it:
                visited.append(next_vertex)
                unvisited.remove(next_vertex)
                
                self.branch_and_bound(
                    current_vertex=next_vertex,
                    unvisited=unvisited,
                    visited=visited,
                    current_cost=current_cost + self._graph.get_cost(current_vertex, next_vertex),
                )
                
                visited.remove(next_vertex)
                unvisited.append(next_vertex)
        
    @abstractmethod
    def bound(self, current_vertex: int, unvisited: List[int]) -> int:
        pass
    
    def iterator(self, current_vertex: int, unvisited: List[int], graph: Graph) -> Iterator[int]:
        pass