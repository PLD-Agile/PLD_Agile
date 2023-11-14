from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4


@dataclass
class DeliveryMan:
    name: str
    availabilities: List[int]
    id: UUID = field(default_factory=uuid4)
