from dataclasses import dataclass
from typing import Type, TypeVar, Generic
from enum import Enum

from PyQt6.QtWidgets import QWidget

RouteName = TypeVar("RouteName", Enum, str)


@dataclass
class Route(Generic[RouteName]):
    name: RouteName
    widget: Type[QWidget]
