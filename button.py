from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QFont, QCursor
from PyQt6.QtCore import Qt

BUTTONS_FONT = QFont("@Microsoft JhengHei UI", 11)
BUTTONS_ACTIVE_STYLE = """
QPushButton {
    background-color: #8a99a9;
}

QPushButton:hover {
    background-color: white;
}

QPushButton:pressed {
    background-color: #e0eaf4;
}
"""
BUTTONS_INACTIVE_STYLE = """
QPushButton {
    background-color: #6c7b8b;
}

QPushButton:hover {
    background-color: #6c7b8b;
}

QPushButton:pressed {
    background-color: #6c7b8b;
}
"""


class Button(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFont(BUTTONS_FONT)
        self.setStyleSheet(BUTTONS_INACTIVE_STYLE)
        self.setEnabled(False)


    def activate_button(self):
        self.setStyleSheet(BUTTONS_ACTIVE_STYLE)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setEnabled(True)


    def inactivate_button(self):
        self.setStyleSheet(BUTTONS_INACTIVE_STYLE)
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.setEnabled(False)