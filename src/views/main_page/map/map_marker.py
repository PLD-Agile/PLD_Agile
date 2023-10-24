from PyQt6.QtWidgets import QAbstractGraphicsShapeItem
from dataclasses import dataclass

AlignBottom = bool


@dataclass
class MapMarker:
    shape: QAbstractGraphicsShapeItem
    align_bottom: AlignBottom
    scale: float
