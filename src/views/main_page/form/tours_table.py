from typing import Dict, List

from PyQt6.QtWidgets import QLabel, QTableWidget

from src.models.tour import Tour
from src.views.main_page.form.tours_table_column import ToursTableColumn
from src.views.main_page.form.tours_table_column_items import (
    ToursTableColumnItemActions,
    ToursTableColumnItemAddress,
    ToursTableColumnItemDeliveryMan,
    ToursTableColumnItemTime,
    ToursTableColumnItemTour,
)


class ToursTable(QTableWidget):
    COLUMNS: List[ToursTableColumn] = [
        ToursTableColumn(
            header="Tour",
            render=ToursTableColumnItemTour,
            width=40,
        ),
        ToursTableColumn(
            header="Adresse",
            render=ToursTableColumnItemAddress,
            width=200,
        ),
        ToursTableColumn(
            header="Heure",
            render=ToursTableColumnItemTime,
        ),
        ToursTableColumn(
            header="Livreur",
            render=ToursTableColumnItemDeliveryMan,
            width=150,
        ),
        ToursTableColumn(
            header="",
            render=ToursTableColumnItemActions,
            width=80
        ),
    ]

    def __init__(self):
        super().__init__()
        self.__setup_table()

    def update_content(self, tours: List[Tour]) -> None:
        self.setRowCount(0)

        for tour in tours:
            for delivery in tour.deliveries.values():
                row = self.rowCount()

                self.insertRow(row)

                for column, column_factory in enumerate(self.COLUMNS):
                    self.setCellWidget(
                        row, column, column_factory.render(tour, delivery)
                    )

    def __setup_table(self):
        self.setColumnCount(len(self.COLUMNS))
        self.setHorizontalHeaderLabels([column.header for column in self.COLUMNS])
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)

        for i, col in enumerate(self.COLUMNS):
            if col.width is not None:
                self.setColumnWidth(i, col.width)
