from abc import ABC, abstractmethod

class Graph(ABC):
    """Get the number of vertices in the graph.

    Returns:
        the number of vertices in this
    """
    @abstractmethod
    def get_nb_vertices(self) -> int:
        pass
    
    """Get cost
    
    Args:
        i: the source vertex
        j: the destination vertex
    
    Returns:
        the cost of arc (i,j) if (i,j) is an arc; -1 otherwise
    """
    @abstractmethod
    def get_cost(self, i: int, j: int) -> int:
        pass
    
    """Is arc
    
    Args:
        i: the source vertex
        j: the destination vertex
        
    Returns:
        true if (i,j) is an arc of this; false otherwise
    """
    @abstractmethod
    def is_arc(self, i: int, j: int) -> bool:
        pass