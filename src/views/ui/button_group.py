from typing import List
from PyQt6 import QtCore
from PyQt6.QtWidgets import QHBoxLayout, QWidget
from src.views.ui.button import Button, ButtonCorners


class ButtonGroup(QWidget):
    def __init__(self, buttons: List[Button]) -> None:
        super().__init__()

        layout = QHBoxLayout()

        layout.setSpacing(1)

        self.setLayout(layout)

        for i, button in enumerate(buttons):
            print(i, button)
            if i == 0:
                print("LEFT")
                button.setCorners(ButtonCorners.LEFT)
            elif i == len(buttons) - 1:
                print("RIGHT")
                button.setCorners(ButtonCorners.RIGHT)
            else:
                print("NONE")
                button.setCorners(ButtonCorners.NONE)

            layout.addWidget(button)
