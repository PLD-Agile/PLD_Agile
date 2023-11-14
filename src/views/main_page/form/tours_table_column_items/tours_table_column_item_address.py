from PyQt6.QtWidgets import QLabel

from src.models.tour import Tour, Delivery


class ToursTableColumnItemAddress(QLabel):
    def __init__(self, tour: Tour, delivery: Delivery):
        super().__init__(delivery.location.segment.name)
