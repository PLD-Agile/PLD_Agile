from PyQt6.QtGui import QIcon, QPixmap, QColor
from PyQt6.QtCore import Qt
import qtawesome as qta
from typing import Optional


def get_icon_pixmap(
    icon: QIcon | str, size: int = 16, color: Optional[QColor] = None
) -> QPixmap:
    pixmap = qta.icon(f"fa5s.{icon}" if isinstance(icon, str) else icon).pixmap(
        size, size
    )

    if color:
        mask = pixmap.createMaskFromColor(
            Qt.GlobalColor.transparent, Qt.MaskMode.MaskInColor
        )
        pixmap.fill(color)
        pixmap.setMask(mask)

    return pixmap
