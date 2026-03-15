from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap, QFont, QCursor
from PyQt6.QtCore import Qt

BUTTONS_FONT = QFont("@Microsoft JhengHei UI", 10)

class Button(QFrame):
    def __init__(self, pixmap_path_disabled, pixmap_path_enabled, pixmap_path_hover, text, function, parent=None):
        super().__init__(parent)
        self.setObjectName("button")
        self.setFixedSize(70,70)

        self.pixmap_enabled = QPixmap(pixmap_path_enabled).scaled(24, 24)
        self.pixmap_disabled = QPixmap(pixmap_path_disabled).scaled(24, 24)
        self.pixmap_hover = QPixmap(pixmap_path_hover).scaled(24, 24)

        self.icon = QLabel(self)
        self.icon.setPixmap(self.pixmap_disabled)
        self.icon.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.text = QLabel(text)
        self.text.setFont(BUTTONS_FONT)
        self.text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10,10,10,10)

        layout.addWidget(self.icon)
        layout.addWidget(self.text)

        self.function = function

        self.setEnabled(False)
        self.text.setEnabled(self.isEnabled())

        self._pressed_inside = False


    def setEnabled(self, enabled: bool):
        super().setEnabled(enabled)

        self.text.setEnabled(enabled)

        if enabled:
            self.icon.setPixmap(self.pixmap_enabled)
            self.text.setStyleSheet("color: white")
            self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        else:
            self.icon.setPixmap(self.pixmap_disabled)
            self.text.setStyleSheet("color: #304051")
            self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed_inside = True
            self.setStyleSheet("background-color: #c8daec")
        super().mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self._pressed_inside:
            if self.rect().contains(event.position().toPoint()):
                self.function()
                self.setStyleSheet("")
        self._pressed_inside = False
        super().mouseReleaseEvent(event)


    def enterEvent(self, event):
        if self.isEnabled():
            self.icon.setPixmap(self.pixmap_hover)
            self.text.setStyleSheet("color: black")
        super().enterEvent(event)


    def leaveEvent(self, event):
        if self.isEnabled():
            self.icon.setPixmap(self.pixmap_enabled)
            self.text.setStyleSheet("color: white")
        super().leaveEvent(event)