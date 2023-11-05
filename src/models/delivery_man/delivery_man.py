from dataclasses import dataclass
from typing import List


@dataclass
class DeliveryMan:
    name: str
    availabilities: List[int]
