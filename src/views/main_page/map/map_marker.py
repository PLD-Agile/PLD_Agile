from dataclasses import dataclass

from PyQt6.QtWidgets import QAbstractGraphicsShapeItem

AlignBottom = bool


@dataclass
class MapMarker:
    shape: QAbstractGraphicsShapeItem
    align_bottom: AlignBottom
    scale: float
