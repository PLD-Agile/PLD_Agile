from dataclasses import dataclass
from typing import Dict

from src.models.map.intersection import Intersection


@dataclass
class Tour:
    delivery_man: str
    deliveries: Dict[int, Intersection]
