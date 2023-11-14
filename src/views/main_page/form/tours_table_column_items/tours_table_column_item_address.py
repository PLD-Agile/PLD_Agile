from PyQt6.QtWidgets import QLabel

from src.models.tour import Delivery


class ToursTableColumnItemAddress(QLabel):
    def __init__(self, delivery: Delivery):
        super().__init__(delivery.location.segment.name)
