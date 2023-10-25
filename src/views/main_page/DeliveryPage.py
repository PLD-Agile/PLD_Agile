from PyQt6.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, 
                             QComboBox, QTableWidget, QTableWidgetItem, QWidget, 
                             QVBoxLayout, QSpacerItem, QSizePolicy, QTableWidgetItem)
from PyQt6.QtCore import Qt

from src.controllers.navigator.page import Page

class DeliveryPage(Page):
    def __init__(self):
        super().__init__()

        #  Delivery Man et Time Window
        self.delivery_man_label = QLabel("<b>Delivery Man:</b>")
        self.delivery_man_combobox = QComboBox()
        self.delivery_man_combobox.addItem("Josué stcyr")
        self.delivery_man_combobox.addItem("clem farhat")

        self.time_window_label = QLabel("<b>Time Window:</b>")
        self.time_window_combobox = QComboBox()
        self.time_window_combobox.addItem("8:00 AM - 9:00 AM")
        self.time_window_combobox.addItem("9:00 AM - 10:00 AM")
        self.time_window_combobox.addItem("10:00 AM - 11:00 AM")
        self.time_window_combobox.addItem("11:00 AM - 12:00 PM")

        #  Delivery Address
        self.address_input = QLineEdit()
        self.add_address_button = QPushButton("Add Address")
        self.add_address_button.clicked.connect(self.add_address)

        # Tableau 
        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Delivery Address", "Time Window", "Delivery Man"])

        #  Compute Tour
        compute_tour_button = QPushButton("Compute Tour")
        compute_tour_button.clicked.connect(self.compute_tour)

  
        layout = QVBoxLayout()

        for widget in [self.delivery_man_label, self.delivery_man_combobox, self.time_window_label, self.time_window_combobox, self.address_input, self.add_address_button]:
            widget.setStyleSheet("color: black;")
            layout.addWidget(widget)

        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        layout.addSpacerItem(spacer)

        layout.addWidget(self.table_widget)
        layout.addWidget(compute_tour_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(layout)

     
        self.address_list = []

    def add_address(self):
        address = self.address_input.text()
        delivery_man = self.delivery_man_combobox.currentText()
        time_window = self.time_window_combobox.currentText()

        if address:
            self.address_list.append((address, time_window, delivery_man))

            # tableau
            row_position = self.table_widget.rowCount()
            self.table_widget.insertRow(row_position)
            self.table_widget.setItem(row_position, 0, QTableWidgetItem(address))
            self.table_widget.setItem(row_position, 1, QTableWidgetItem(time_window))
            self.table_widget.setItem(row_position, 2, QTableWidgetItem(delivery_man))

            self.address_input.clear()

    def compute_tour(self):
        pass

    def remove_address(self, row):
        pass
