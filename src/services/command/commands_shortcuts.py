from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QWidget

from src.services.command.command_service import CommandService


def init_commands_shortcuts(widget: QWidget):
    QShortcut(QKeySequence.StandardKey.Undo, widget).activated.connect(
        lambda: CommandService.instance().undo()
    )
    QShortcut(QKeySequence.StandardKey.Redo, widget).activated.connect(
        lambda: CommandService.instance().redo()
    )
