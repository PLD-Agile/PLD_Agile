from PyQt6.QtWidgets import QWidget


class Page(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def on_page_enter(self):
        """Method called when the navigator shows this page."""
        pass

    def on_page_leave(self):
        """Method called when the navigator hides this page. This method can be called event if the page stays in the history stack."""
        pass
