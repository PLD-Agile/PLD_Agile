from dataclasses import dataclass, field
from typing import List
import uuid

@dataclass
class DeliveryMan:
    name: str
    availabilities: List[int]
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
