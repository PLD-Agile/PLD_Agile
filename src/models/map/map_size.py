import sys
from dataclasses import dataclass
from typing import Type, TypeVar

from src.models.map.position import Position

T = TypeVar("T", bound="MapSize")


@dataclass
class MapSize:
    """Represents the size of a map.
    """
    __min: Position
    __max: Position
    area: float

    def __init__(self, min: Position, max: Position) -> None:
        self.__min = min
        self.__max = max
        self.area = self.__calculate_area()

    @classmethod
    def inverse_max_size(cls: Type[T]) -> T:
        """Creates a MapSize instance with the inverted maximum possible size. (min = System MAX, max = System MIN)"""
        return cls(
            Position(sys.maxsize, sys.maxsize),
            Position(sys.maxsize * -1, sys.maxsize * -1),
        )

    @property
    def min(self) -> Position:
        return self.__min

    @min.setter
    def min(self, value: Position) -> None:
        self.__min = value
        self.area = self.__calculate_area()

    @property
    def max(self) -> Position:
        return self.__max

    @max.setter
    def max(self, value: Position) -> None:
        self.__max = value
        self.area = self.__calculate_area()

    @property
    def width(self) -> float:
        return self.__max.longitude - self.__min.longitude

    @property
    def height(self) -> float:
        return self.__max.latitude - self.__min.latitude

    def __calculate_area(self) -> float:
        return (self.__max.latitude - self.__min.latitude) * (
            self.__max.longitude - self.__min.longitude
        )
