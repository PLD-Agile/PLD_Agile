from PyQt6.QtWidgets import QFrame, QWidget


class Separator(QFrame):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Plain)
        self.setStyleSheet(
            """
            color: #515764;
        """
        )
