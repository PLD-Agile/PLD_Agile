from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLayout,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from src.controllers.navigator.page import Page
from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.tour import TourRequest
from src.services.tour.tour_service import TourService
from src.views.ui import Button, Callout, Separator, Text, TextSize

DELIVERY_MAN: List[DeliveryMan] = [
    DeliveryMan("Josué stcyr", [8, 9, 10, 11]),
    DeliveryMan("clem farhat", [8, 9]),
]


class DeliveryFormPage(Page):
    __delivery_man_control: QComboBox
    __time_window_control: QComboBox
    __delivery_table: QTableWidget

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(Text("Add deliveries", TextSize.H1))
        layout.addLayout(self.__build_delivery_man_form())
        layout.addWidget(
            Callout(
                "Double-click on the map to add deliveries with the selected delivery man and time"
            )
        )
        layout.addWidget(Text("Deliveries", TextSize.H1))
        layout.addLayout(self.__build_delivery_table())
        layout.addWidget(Separator())
        layout.addLayout(self.__build_load_tour())

        self.setLayout(layout)

        self.address_list = []

        self.__update_delivery_man_combobox(DELIVERY_MAN)
        TourService.instance().tour_requests.subscribe(self.__update_delivery_table)

    def compute_tour(self):
        TourService.instance().compute_tours()

    def remove_address(self, row):
        pass

    def __build_delivery_man_form(self) -> QLayout:
        layout = QHBoxLayout()

        delivery_man_layout = QVBoxLayout()
        delivery_man_label = Text("Delivery man", TextSize.label)
        delivery_man_combobox = QComboBox()

        time_window_layout = QVBoxLayout()
        time_window_label = Text("Time window", TextSize.label)
        time_window_combobox = QComboBox()

        delivery_man_layout.addWidget(delivery_man_label)
        delivery_man_layout.addWidget(delivery_man_combobox)

        time_window_layout.addWidget(time_window_label)
        time_window_layout.addWidget(time_window_combobox)

        layout.addLayout(delivery_man_layout)
        layout.addLayout(time_window_layout)

        layout.setContentsMargins(0, 0, 0, 0)
        delivery_man_layout.setContentsMargins(0, 0, 0, 0)
        delivery_man_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        time_window_layout.setContentsMargins(0, 0, 0, 0)
        time_window_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.__delivery_man_control = delivery_man_combobox
        self.__time_window_control = time_window_combobox

        delivery_man_combobox.currentIndexChanged.connect(
            lambda: self.__update_time_window_combobox(
                delivery_man_combobox.currentData()
            )
        )

        return layout

    def __build_delivery_table(self) -> QLayout:
        layout = QVBoxLayout()

        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(
            ["Delivery Address", "Time Window", "Delivery Man"]
        )
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        self.__delivery_table = table

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        compute_tour_button = Button("Compute Tour")
        compute_tour_button.clicked.connect(self.compute_tour)

        buttons_layout.addWidget(compute_tour_button)

        layout.addWidget(table)
        layout.addLayout(buttons_layout)

        return layout

    def __build_load_tour(self) -> QLayout:
        layout = QVBoxLayout()

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        compute_tour_button = Button("Load Tour")

        buttons_layout.addWidget(compute_tour_button)

        layout.addWidget(
            Callout(
                "Or load an existing tour (this will overwrite any destinations above)"
            )
        )
        layout.addLayout(buttons_layout)

        return layout

    def __update_delivery_man_combobox(self, delivery_mans: List[DeliveryMan]) -> None:
        current_value = self.__delivery_man_control.currentData()
        self.__delivery_man_control.clear()

        for delivery_man in delivery_mans:
            self.__delivery_man_control.addItem(delivery_man.name, delivery_man)

        new_index = max(self.__delivery_man_control.findData(current_value), 0)

        self.__delivery_man_control.setCurrentIndex(new_index)

    def __update_time_window_combobox(self, delivery_man: DeliveryMan) -> None:
        current_value = self.__time_window_control.currentData()
        self.__time_window_control.clear()

        for time_window in delivery_man.availabilities:
            self.__time_window_control.addItem(
                f"{time_window}:00 - {time_window + 1}:00", time_window
            )

        if current_value:
            self.__time_window_control.setCurrentIndex(
                max(self.__time_window_control.findData(current_value), 0)
            )

    def __update_delivery_table(self, tours: List[TourRequest]) -> None:
        self.__delivery_table.setRowCount(0)

        for tour in tours:
            for delivery in tour.deliveries:
                row_position = self.__delivery_table.rowCount()

                timeWindow = f"{delivery.timeWindow}:00 - {delivery.timeWindow + 1}:00"

                self.__delivery_table.insertRow(row_position)
                self.__delivery_table.setItem(
                    row_position, 0, QTableWidgetItem(delivery.location.segment.name)
                )
                self.__delivery_table.setItem(
                    row_position, 1, QTableWidgetItem(timeWindow)
                )
                self.__delivery_table.setItem(
                    row_position, 2, QTableWidgetItem(tour.delivery_man.name)
                )
