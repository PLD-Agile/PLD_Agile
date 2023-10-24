import sys

from PyQt6.QtWidgets import QApplication

from src.views.window import MainWindow
from views.modules.navigators import init_navigators

app = QApplication(sys.argv)

init_navigators()

window = MainWindow()
window.show()

app.exec()
