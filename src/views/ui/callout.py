from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget


class Callout(QLabel):
    STYLE_SHEET = """
        color: #ffffff;
        background-color: #515764;
        font-weight: 500;
        padding: 12px;
        border-radius: 3px;
    """

    def __init__(self, text: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent=parent)
        self.setStyleSheet(self.STYLE_SHEET)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
