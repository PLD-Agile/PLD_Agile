from dataclasses import dataclass
from enum import Enum
from typing import Generic, Type, TypeVar

from PyQt6.QtWidgets import QWidget

RouteName = TypeVar("RouteName", Enum, str)


@dataclass
class Route(Generic[RouteName]):
    name: RouteName
    widget: Type[QWidget]
