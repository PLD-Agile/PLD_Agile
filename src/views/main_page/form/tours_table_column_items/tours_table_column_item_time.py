from typing import Dict

from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QWidget

from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.tour import ComputedDelivery, Delivery, Tour
from src.services.delivery_man.delivery_man_service import DeliveryManService
from src.services.tour.tour_service import TourService


class ToursTableColumnItemTime(QWidget):
    __tour: Tour
    __delivery: Delivery
    __time_control: QComboBox

    def __init__(self, tour: Tour, delivery: Delivery):
        super().__init__()

        self.__tour = tour
        self.__delivery = delivery

        self.__build()

        delivery_man_subscription = (
            DeliveryManService.instance().delivery_men.subscribe(
                lambda _: self.__update_time_control_items()
            )
        )

        self.destroyed.connect(lambda: delivery_man_subscription.dispose())

    def __build(self):
        self.__build_time_control()

        layout = QHBoxLayout()
        layout.addWidget(self.__time_control)
        layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(layout)

    def __build_time_control(self):
        self.__time_control = QComboBox()

    def __update_time_control_items(self):
        self.__time_control.clear()

        try:
            self.__time_control.currentIndexChanged.disconnect()
        except TypeError:
            pass

        for i, availability in enumerate(self.__tour.delivery_man.availabilities):
            if (
                isinstance(self.__delivery, ComputedDelivery)
                and self.__delivery.time.hour == availability
            ):
                self.__time_control.addItem(
                    self.__delivery.time.strftime("%H:%M"), userData=-1
                )
                self.__time_control.setCurrentIndex(i)
            else:
                self.__time_control.addItem(
                    f"{availability}:00 - {availability + 1}:00", userData=availability
                )

        self.__time_control.currentIndexChanged.connect(
            lambda: self.__handle_time_change(self.__time_control.currentData())
        )

    def __handle_time_change(self, time_window: int):
        if time_window is None or time_window == -1:
            return

        TourService.instance().update_delivery_request_time_window(
            delivery_request_id=self.__delivery.id,
            tour_id=self.__tour.id,
            time_window=time_window,
        )
