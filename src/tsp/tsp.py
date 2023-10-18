from abc import ABC, abstractmethod

from src.graph.graph import Graph


class TSP(ABC):
    """Search for a shortest cost hamiltonian circuit in <code>g</code> within <code>timeLimit</code> milliseconds
    (returns the best found tour whenever the time limit is reached)
    Warning: The computed tour always start from vertex 0
    """

    @abstractmethod
    def search_solution(self, time_limit: int, graph: Graph) -> None:
        pass

    """Get solution
    
    Returns:
        the ith visited vertex in the solution computed by <code>searchSolution</code> 
        (-1 if <code>searcheSolution</code> has not been called yet, or if i < 0 or i >= g.getNbSommets())
    """

    @abstractmethod
    def get_solution(self, i: int) -> int:
        pass

    """Get solution cost
    
    Returns:
        the total cost of the solution computed by <code>searchSolution</code>
        (-1 if <code>searcheSolution</code> has not been called yet). 
    """

    @abstractmethod
    def get_solution_cost(self) -> int:
        pass
