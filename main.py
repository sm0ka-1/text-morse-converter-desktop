import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, \
    QTextEdit
from PyQt6.QtGui import QFont, QPixmap, QTextCursor, QTextCharFormat, QColor
from PyQt6.QtCore import Qt
from button import Button
from converter import text_to_morse, morse_to_text
from morse_player import MorsePlayer

TITLE_FONT = QFont("Agency FB", 60)
SUBTITLE_FONT = QFont("Agency FB", 32)
LABEL_FONT = QFont("@Microsoft JhengHei UI", 13)
ERROR_LABEL_FONT = QFont("@Microsoft JhengHei UI", 11)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.player = MorsePlayer()
        self.player.something_changed.connect(self.update_buttons)
        self.player.highlight_changed.connect(self.update_highlight)

        self.initialize_ui()


    def initialize_ui(self):
        self.setGeometry(100,50,840,530)
        self.setWindowTitle("Text To Morse Code Converter")
        self.generate_window()
        self.show()


    def generate_window(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(50, 30, 50, 30)
        main_widget.setLayout(main_layout)

        title = self.build_title()

        main_layout.addWidget(title)
        main_layout.addSpacing(30)
        main_layout.addStretch(1)

        converters_layout = self.build_converters()
        main_layout.addLayout(converters_layout)

        buttons_layout = self.build_buttons()
        main_layout.addSpacing(20)
        main_layout.addLayout(buttons_layout)

        self.error_label = self.build_error_label()

        main_layout.addStretch(2)
        main_layout.addWidget(self.error_label)
        main_layout.addStretch(4)

        with open("styles.css", "r") as file:
            styles = file.read()
        self.setStyleSheet(styles)


    # -------------------------------- UI SETUP -------------------------------- #

    def build_title(self):
        # WIDGETS
        title = QWidget()

        title_left = QLabel("TEXT")
        title_left.setFont(TITLE_FONT)
        title_left.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        title_left.setObjectName("title_left")

        telegraph_img = QLabel()
        telegraph_pixmap = QPixmap("./assets/images/telegraph.png")
        telegraph_pixmap = telegraph_pixmap.scaledToHeight(61, Qt.TransformationMode.SmoothTransformation)
        telegraph_img.setPixmap(telegraph_pixmap)
        telegraph_img.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        telegraph_img.setContentsMargins(0,13,0,0)

        title_right = QLabel("MORSE")
        title_right.setFont(TITLE_FONT)
        title_right.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        title_right.setObjectName("title_right")

        title_middle = QLabel("CONVERTER")
        title_middle.setFont(SUBTITLE_FONT)
        title_middle.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        title_middle.setObjectName("title_middle")

        # LAYOUT
        title_layout = QHBoxLayout()
        title_layout.setContentsMargins(0,0,0,0)
        title.setLayout(title_layout)

        title_center_layout = QVBoxLayout()
        title_center_layout.setContentsMargins(0,0,0,0)
        title_center_layout.addWidget(telegraph_img)
        title_center_layout.addWidget(title_middle)

        title_layout.addStretch(1)
        title_layout.addSpacing(54)
        title_layout.addWidget(title_left)
        title_layout.addLayout(title_center_layout)
        title_layout.addWidget(title_right)
        title_layout.addStretch(1)

        return title


    def build_converters(self):
        # WIDGETS
        input_text_label = QLabel("Write or paste your text:")
        input_text_label.setFont(LABEL_FONT)

        self.text_box = QTextEdit()
        self.text_box.setFont(LABEL_FONT)
        self.text_box.setMaximumHeight(250)
        self.text_box.setMaximumWidth(500)
        self.text_box.textChanged.connect(self.handle_text_box_change)

        input_morse_label = QLabel("Write or paste your morse code:")
        input_morse_label.setFont(LABEL_FONT)

        self.morse_box = QTextEdit()
        self.morse_box.setFont(LABEL_FONT)
        self.morse_box.setMaximumHeight(250)
        self.morse_box.setMaximumWidth(500)
        self.morse_box.textChanged.connect(self.handle_morse_box_change)

        # LAYOUT
        converters_layout = QHBoxLayout()
        text_area_layout = QVBoxLayout()
        morse_area_layout = QVBoxLayout()

        text_area_layout.addWidget(input_text_label)
        text_area_layout.addWidget(self.text_box)

        morse_area_layout.addWidget(input_morse_label)
        morse_area_layout.addWidget(self.morse_box)

        converters_layout.addStretch()
        converters_layout.addLayout(text_area_layout, stretch=1)
        converters_layout.addLayout(morse_area_layout, stretch=1)
        converters_layout.addStretch()

        return converters_layout


    def build_buttons(self):
        buttons_layout = QHBoxLayout()

        path = "./assets/images/"

        self.play_button = Button(f"{path}play_disabled.png", f"{path}play_enabled.png", f"{path}play_hover.png", "Play", lambda: self.player.play(self.morse_box.toPlainText()))
        self.pause_button = Button(f"{path}pause_disabled.png", f"{path}pause_enabled.png", f"{path}play_hover.png", "Pause", self.player.pause)
        self.stop_button = Button(f"{path}stop_disabled.png", f"{path}stop_enabled.png", f"{path}play_hover.png", "Stop", self.player.stop)
        self.clear_button = Button(f"{path}bin_disabled.png", f"{path}bin_enabled.png", f"{path}bin_hover.png", "Clear", self.handle_clear_button_click)

        buttons_layout.addStretch()
        buttons_layout.addWidget(self.play_button)
        buttons_layout.addWidget(self.pause_button)
        buttons_layout.addWidget(self.stop_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addStretch()

        return buttons_layout


    def build_error_label(self):
        error_label = QLabel()
        error_label.setFont(ERROR_LABEL_FONT)
        error_label.setContentsMargins(0, 10, 0, 0)
        error_label.setMinimumHeight(60)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setObjectName("error_label")

        return error_label


    def handle_text_box_change(self):
        self.update_buttons()
        self.delete_error_message()
        try:
            morse = text_to_morse(self.text_box.toPlainText())
            if self.morse_box.toPlainText() != morse:
                if self.player.is_playing:
                    self.player.stop()
                self.morse_box.blockSignals(True)
                self.morse_box.setPlainText(morse)
                self.morse_box.blockSignals(False)
        except ValueError as e:
            self.show_error_message(str(e))
            self.morse_box.blockSignals(True)
            self.morse_box.setPlainText("")
            self.morse_box.blockSignals(False)


    def handle_morse_box_change(self):
        self.update_buttons()
        self.delete_error_message()
        try:
            text = morse_to_text(self.morse_box.toPlainText())
            if self.text_box.toPlainText() != text and self.text_box.toPlainText().upper() != text:
                if self.player.is_playing:
                    self.player.stop()
                self.text_box.blockSignals(True)
                self.text_box.setPlainText(text)
                self.text_box.blockSignals(False)
        except ValueError as e:
            self.show_error_message(str(e))
            self.text_box.blockSignals(True)
            self.text_box.setPlainText("")
            self.text_box.blockSignals(False)


    def handle_clear_button_click(self):
        if self.player.is_playing:
            self.player.stop()
            self.player.currentIndex = 0

        self.text_box.setPlainText("")
        self.morse_box.setPlainText("")
        self.update_buttons()
        self.delete_error_message()


    def update_buttons(self):
        text = self.text_box.toPlainText().strip()
        morse = self.morse_box.toPlainText().strip()
        playable_morse = self.is_playable_morse_code(morse) if morse else False

        self.clear_button.setEnabled(bool(text) or bool(morse))
        self.play_button.setEnabled(playable_morse and not self.player.is_playing)
        self.pause_button.setEnabled(playable_morse and self.player.is_playing)
        self.stop_button.setEnabled(self.player.is_playing or self.player.currentIndex > 0)


    def is_playable_morse_code(self, morse_code):
        allowed = {'.', '-', ' ', '/', '\n'}
        if any(ch not in allowed for ch in morse_code):
            return False
        else:
            return True


    def show_error_message(self, message):
        self.error_label.setText(message)
        if self.player.is_playing:
            self.player.stop()


    def delete_error_message(self):
        self.error_label.setText("")


    def update_highlight(self, index: int):
        text = self.morse_box.toPlainText()

        if index < 0 or index >= len(text):
            self.morse_box.setExtraSelections([])
            return

        cursor = self.morse_box.textCursor()
        cursor.setPosition(index)
        cursor.movePosition(QTextCursor.MoveOperation.Right,
                            QTextCursor.MoveMode.KeepAnchor, 1)
        highlight = QTextEdit.ExtraSelection()
        highlight.cursor = cursor

        fmt = QTextCharFormat()
        fmt.setBackground(QColor(96, 189, 255, 128))
        highlight.format = fmt

        self.morse_box.setExtraSelections([highlight])

        # Scroll synchronization
        highlight_rect = self.morse_box.cursorRect(cursor)
        viewport_rect = self.morse_box.viewport().rect()
        scrollbar = self.morse_box.verticalScrollBar()

        if highlight_rect.bottom() > viewport_rect.bottom():
            scrollbar.setValue(scrollbar.value() + highlight_rect.bottom() - viewport_rect.bottom())
        elif highlight_rect.top() < viewport_rect.top():
            scrollbar.setValue(scrollbar.value() - viewport_rect.top() + highlight_rect.top())



if  __name__ == '__main__':
    app  = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
