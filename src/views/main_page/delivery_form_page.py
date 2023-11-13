import time
from typing import Dict, List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLayout,
    QMessageBox,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.controllers.navigator.page import Page
from src.models.delivery_man.delivery_man import DeliveryMan
from src.models.tour import DeliveryRequest, TourRequest
from src.services.command.command_service import CommandService
from src.services.command.commands.remove_delivery_request_command import (
    RemoveDeliveryRequestCommand,
)
from src.services.delivery_man.delivery_man_service import DeliveryManService
from src.services.tour.tour_service import TourService
from src.views.ui import Button, Callout, Separator, Text, TextSize


class DeliveryFormPage(Page):
    __delivery_man_control: QComboBox
    __time_window_control: QComboBox
    __delivery_table: QTableWidget

    def __init__(self):
        super().__init__()

        # Define components to be used in this screen
        layout = QVBoxLayout()
        warehouse_location_label = Text("Warehouse Location", TextSize.H2)
        add_deliveries_label = Text("Add deliveries", TextSize.H2)
        add_deliveries_click = Callout(
            "Double-click on the map to add deliveries with the selected deliveryman and time"
        )

        deliveries_label = Text("Deliveries", TextSize.H2)

        # Add components in the screen
        layout.addWidget(warehouse_location_label)
        layout.addLayout(self.__build_warehouse_location())
        layout.addWidget(Separator())
        layout.addWidget(add_deliveries_label)
        layout.addLayout(self.__build_delivery_man_form())
        layout.addWidget(add_deliveries_click)

        layout.addWidget(deliveries_label)
        layout.addLayout(self.__build_delivery_table())
        layout.addWidget(Separator())
        layout.addLayout(self.__build_load_tours())

        self.setLayout(layout)

        # UNUSED self.address_list = []

        DeliveryManService.instance().delivery_men.subscribe(
            self.__update_delivery_man_combobox
        )
        TourService.instance().tour_requests.subscribe(self.__update_delivery_table)

    def compute_tour(self):
        TourService.instance().compute_tours()

    def remove_delivery(self, delivery: DeliveryRequest, delivery_man: DeliveryMan):
        CommandService.instance().execute(
            RemoveDeliveryRequestCommand(
                delivery_request=delivery,
                delivery_man=delivery_man,
            )
        )
        # TourService.instance().remove_delivery_request(delivery, delivery_man)

    def __build_warehouse_location(self) -> QLayout:
        # Define components to be used in this screen
        layout = QHBoxLayout()

        warehouse_address_label = Text("20 avenue Albert Einstein", TextSize.label)

        layout.addWidget(warehouse_address_label)

        return layout

    def __build_delivery_man_form(self) -> QLayout:
        # Define components to be used in this screen
        layout = QHBoxLayout()

        delivery_man_layout = QVBoxLayout()
        delivery_man_combobox = QComboBox()
        delivery_man_label = Text("Deliveryman", TextSize.label)

        time_window_layout = QVBoxLayout()
        time_window_combobox = QComboBox()
        time_window_label = Text("Time window", TextSize.label)

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

        delivery_man_combobox.currentIndexChanged.connect(
            lambda: DeliveryManService.instance().set_selected_delivery_man(
                delivery_man_combobox.currentData().id
                if delivery_man_combobox.currentData()
                else None
            )
        )
        time_window_combobox.currentIndexChanged.connect(
            lambda: DeliveryManService.instance().set_selected_time_window(
                time_window_combobox.currentData()
            )
        )

        return layout

    def __build_delivery_table(self) -> QLayout:
        # Define components to be used in this screen
        layout = QVBoxLayout()

        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(
            ["Delivery Address", "Time Window", "Delivery Man", ""]
        )
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        self.__delivery_table = table

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        """ compute_tour_button = Button("Compute Tour")
        compute_tour_button.clicked.connect(self.compute_tour) """

        save_tour_button = Button("Save Tour")
        save_tour_button.clicked.connect(self.__save_tour)

        # Add components in the screen
        # buttons_layout.addWidget(compute_tour_button)
        buttons_layout.addWidget(save_tour_button)

        layout.addWidget(table)
        layout.addLayout(buttons_layout)

        return layout

    def __build_load_tours(self) -> QLayout:
        # Define components to be used in this screen
        layout = QVBoxLayout()

        load_tour_label = Callout(
            "Or load an existing tour to the current deliveryman and current delivery window"
        )

        buttons_layout = QHBoxLayout()
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        load_tour_button = Button("Load Tour")
        buttons_layout.addWidget(load_tour_button)

        layout.addWidget(load_tour_label)
        layout.addLayout(buttons_layout)

        return layout

    def __update_delivery_man_combobox(
        self, delivery_men: Dict[str, DeliveryMan]
    ) -> None:
        current_value = self.__delivery_man_control.currentData()
        self.__delivery_man_control.clear()

        for delivery_man in delivery_men.values():
            self.__delivery_man_control.addItem(delivery_man.name, delivery_man)

        new_index = max(self.__delivery_man_control.findData(current_value), 0)

        self.__delivery_man_control.setCurrentIndex(new_index)

    def __update_time_window_combobox(self, delivery_man: DeliveryMan) -> None:
        current_value = self.__time_window_control.currentData()
        self.__time_window_control.clear()

        if not delivery_man:
            return

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

        self.table_rows = [
            (tour, delivery) for tour in tours for delivery in tour.deliveries
        ]

        for tour, delivery in self.table_rows:
            row_position = self.__delivery_table.rowCount()

            timeWindow = f"{delivery.timeWindow}:00 - {delivery.timeWindow + 1}:00"

            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            remove_btn = Button("Remove")

            remove_btn.clicked.connect(
                lambda: self.remove_delivery(delivery, tour.delivery_man)
            )

            actions_layout.setContentsMargins(2, 2, 2, 2)

            actions_layout.addWidget(remove_btn)
            actions_widget.setLayout(actions_layout)

            self.__delivery_table.insertRow(row_position)

            self.__delivery_table.setItem(
                row_position, 0, QTableWidgetItem(delivery.location.segment.name)
            )
            self.__delivery_table.setItem(row_position, 1, QTableWidgetItem(timeWindow))
            self.__delivery_table.setItem(
                row_position, 2, QTableWidgetItem(tour.delivery_man.name)
            )
            self.__delivery_table.setCellWidget(
                row_position,
                3,
                actions_widget,
            )

        def select_delivery_request(row_index: int) -> None:
            TourService.instance().select_delivery_request(
                self.table_rows[row_index][1].location
            )

        self.__delivery_table.itemSelectionChanged.connect(
            lambda: select_delivery_request(self.__delivery_table.currentRow())
        )

        self.__delivery_table.clearSelection()
        TourService.instance().select_delivery_request(None)

    def __save_tour(self):
        selected_delivery_man: DeliveryMan = self.__delivery_man_control.currentData()
        selected_time_window: int = self.__time_window_control.currentData()

        if selected_delivery_man and selected_time_window:
            delivery_man_name = selected_delivery_man.name
            time_window_str = (
                f"{selected_time_window}:00 - {selected_time_window + 1}:00"
            )
            message = (
                f"Tour saved for {delivery_man_name} with time window {time_window_str}"
            )

            self.__show_popup("Tour Saved", message)
        else:
            self.__show_popup(
                "Error",
                "Please select a delivery man and time window before saving the tour",
            )

    def __show_popup(self, title, message):
        popup = QMessageBox()
        popup.setWindowTitle(title)
        popup.setText(message)
        popup.exec()
