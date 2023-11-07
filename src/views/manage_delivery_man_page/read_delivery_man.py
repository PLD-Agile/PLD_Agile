from typing import Dict
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel
from reactivex import Observer
from models.delivery_man.delivery_man import DeliveryMan
from src.views.ui import Text, TextSize
from src.services.delivery_man.delivery_man_service import DeliveryManService

class ReadDeliveryMan(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        title_label = Text("List of deliverymen", TextSize.H2)

        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.addWidget(title_label)

        self.__delivery_men_list = QVBoxLayout()
        layout.addLayout(self.__delivery_men_list)

        self.setLayout(layout)

        # Create an observer to update the delivery men list
        delivery_observable = DeliveryManService.instance().delivery_men
        delivery_observable.subscribe(self.__update_delivery_man_list)

    def __build_deliverymen_list(self, delivery_men: Dict[str, DeliveryMan]) -> None:
        # Clear the existing list
        for i in reversed(range(self.__delivery_men_list.count())):
            widget = self.__delivery_men_list.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

        for index, deliveryMan in enumerate(delivery_men.values()):
            deliveryManWidget = QLabel(str(index+1) + ".  Name: " + deliveryMan.name)
            self.__delivery_men_list.addWidget(deliveryManWidget)

    def __update_delivery_man_list(self, delivery_men: Dict[str, DeliveryMan]) -> None:
        self.__build_deliverymen_list(delivery_men)