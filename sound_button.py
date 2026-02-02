from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout
from PyQt6.QtGui import QCursor, QPixmap
from PyQt6.QtCore import Qt
from button import BUTTONS_FONT


class SoundButton(QFrame):
    def __init__(self, function, parent=None):
        super().__init__(parent)

        self.is_active = False
        self.style = "play"

        self.play_pixmap = QPixmap("./assets/images/play.png").scaled(24, 24)
        self.play_hover_pixmap = QPixmap("./assets/images/play_hover.png").scaled(24, 24)
        self.stop_pixmap = QPixmap("assets/images/stop.png").scaled(24, 24)
        self.stop_hover_pixmap = QPixmap("assets/images/stop_hover.png").scaled(24, 24)

        self.play_text = "Play morse code"
        self.stop_text = "Stop playing"

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        self.icon = QLabel()
        self.icon.setPixmap(self.play_pixmap)

        self.text = QLabel(self.play_text)
        self.text.setFont(BUTTONS_FONT)

        layout.addWidget(self.icon)
        layout.addWidget(self.text)

        self.setEnabled(False)

        self.function = function


    def mousePressEvent(self, event):
        if self.is_active:
            if event.button() == Qt.MouseButton.LeftButton:
                self.function()
            super().mousePressEvent(event)


    def enterEvent(self, event):
        if self.is_active:
            self.text.setStyleSheet("color: white")
            if self.style == "play":
                self.icon.setPixmap(self.play_hover_pixmap)
            else:
                self.icon.setPixmap(self.stop_hover_pixmap)
        super().enterEvent(event)


    def leaveEvent(self, event):
        self.text.setStyleSheet("color: black")
        if self.style == "play":
            self.icon.setPixmap(self.play_pixmap)
        else:
            self.icon.setPixmap(self.stop_pixmap)
        super().leaveEvent(event)


    def activate_button(self):
        self.is_active = True
        self.setEnabled(True)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))


    def inactivate_button(self):
        self.is_active = False
        self.setEnabled(False)
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))


    def set_play_style(self):
        self.icon.setPixmap(self.play_pixmap)
        self.text.setText(self.play_text)
        self.style = "play"


    def set_stop_style(self):
        self.icon.setPixmap(self.stop_pixmap)
        self.text.setText(self.stop_text)
        self.style = "stop"


