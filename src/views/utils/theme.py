from enum import Enum

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget


class Color(Enum):
    PRIMARY = "#3875ff"
    PRIMARY_CONTRAST = "#ffffff"
    PRIMARY_DISABLED = "#566ea3"
    BACKGROUND = "#2e3440"
    BACKGROUND_CONTRAST = "#ffffff"

    RED = "red"
    GREEN = "green"


class Theme:
    def set_background_color_qt(widget: QWidget, color: QColor):
        widget.setAutoFillBackground(True)
        palette = widget.palette()
        palette.setColor(widget.backgroundRole(), color)
        widget.setPalette(palette)

    def set_background_color(widget: QWidget, color: Color | str):
        Theme.set_background_color_qt(
            widget, QColor(color if isinstance(color, str) else color.value)
        )
