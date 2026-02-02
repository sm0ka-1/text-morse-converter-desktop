import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QTextEdit, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt
from button import Button
from sound_button import SoundButton
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
        self.player.finished_reproduction.connect(self.on_player_finished)

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
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_widget.setLayout(main_layout)

        title = self.build_title()

        main_layout.addWidget(title)
        main_layout.addSpacing(30)
        main_layout.addStretch(1)

        content_layout = self.build_main_content()
        main_layout.addLayout(content_layout)

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


    def build_main_content(self):
        # WIDGETS
        input_text_label = QLabel("Write or paste your text:")
        input_text_label.setFont(LABEL_FONT)

        self.text_box = QTextEdit()
        self.text_box.setFont(LABEL_FONT)
        self.text_box.setMaximumHeight(250)
        self.text_box.textChanged.connect(self.update_text_buttons_state)

        self.to_morse_button = Button("Convert to morse")
        self.to_morse_button.clicked.connect(self.handle_convert_to_morse_click)

        self.delete_text_button = Button()
        self.delete_text_button.setObjectName("delete_text_button")
        self.delete_text_button.clicked.connect(self.handle_delete_text_click)

        input_morse_label = QLabel("Write or paste your morse code:")
        input_morse_label.setFont(LABEL_FONT)

        self.morse_box = QTextEdit()
        self.morse_box.setFont(LABEL_FONT)
        self.morse_box.setMaximumHeight(250)
        self.morse_box.textChanged.connect(self.morse_box_content_changed)

        self.to_text_button = Button("Convert to text")
        self.to_text_button.clicked.connect(self.handle_convert_to_text_click)

        self.delete_morse_button = Button()
        self.delete_morse_button.setObjectName("delete_morse_button")
        self.delete_morse_button.clicked.connect(self.handle_delete_morse_click)

        self.sound_button = SoundButton(self.handle_sound_button_click)
        self.sound_button.setObjectName("sound_button")

        # LAYOUT
        content_layout = QGridLayout()

        content_layout.addWidget(input_text_label, 0, 0)
        content_layout.addWidget(self.text_box, 1, 0)

        to_morse_row = QHBoxLayout()
        to_morse_row.addStretch()
        to_morse_row.addWidget(self.to_morse_button)
        to_morse_row.addWidget(self.delete_text_button)
        content_layout.addLayout(to_morse_row, 2, 0)

        content_layout.addWidget(input_morse_label, 0, 1)
        content_layout.addWidget(self.morse_box, 1, 1)

        to_text_row = QHBoxLayout()
        to_text_row.addStretch()
        to_text_row.addWidget(self.to_text_button)
        to_text_row.addWidget(self.delete_morse_button)
        content_layout.addLayout(to_text_row, 2, 1)

        spacer = QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        content_layout.addItem(spacer, 3, 1)

        sound_row = QHBoxLayout()
        sound_row.addWidget(self.sound_button)
        sound_row.addStretch()
        content_layout.addLayout(sound_row, 4, 1)

        return content_layout


    def build_error_label(self):
        error_label = QLabel("")
        error_label.setFont(ERROR_LABEL_FONT)
        error_label.setContentsMargins(0, 10, 0, 0)
        error_label.setMinimumHeight(60)
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setObjectName("error_label")

        return error_label


    def handle_convert_to_morse_click(self):
        try:
            morse = text_to_morse(self.text_box.toPlainText())
            self.morse_box.setPlainText(morse)
            self.delete_error_message()
        except ValueError as e:
            self.error_label.setText(str(e))


    def handle_convert_to_text_click(self):
        try:
            text = morse_to_text(self.morse_box.toPlainText())
            self.text_box.setPlainText(text)
            self.delete_error_message()
        except KeyError:
            self.error_label.setText("Oops! Invalid morse code.\nAllowed characters: dots ( . ), dashes ( - ) and slashes ( / ) for word spaces.")


    def handle_delete_text_click(self):
        self.text_box.setPlainText("")
        self.delete_error_message()


    def handle_delete_morse_click(self):
        self.morse_box.setPlainText("")
        self.delete_error_message()
        self.stop_reproduction()


    def update_text_buttons_state(self):
        if self.text_box.toPlainText().strip():
            self.to_morse_button.activate_button()
            self.delete_text_button.activate_button()
        else:
            self.to_morse_button.inactivate_button()
            self.delete_text_button.inactivate_button()
        self.delete_error_message()


    def morse_box_content_changed(self):
        text = self.morse_box.toPlainText().strip()
        if self.player.is_playing:
            self.stop_reproduction()

        if text:
            self.to_text_button.activate_button()
            self.delete_morse_button.activate_button()
            self.check_morse_code()
        else:
            self.to_text_button.inactivate_button()
            self.delete_morse_button.inactivate_button()
            self.sound_button.inactivate_button()

        self.delete_error_message()


    def check_morse_code(self):
        text = self.morse_box.toPlainText().strip()
        if text:
            allowed = {'.', '-', ' ', '/'}
            if any(ch not in allowed for ch in text):
                self.sound_button.inactivate_button()
            else:
                self.sound_button.activate_button()


    def delete_error_message(self):
        self.error_label.setText("")


    def handle_sound_button_click(self):
        if not self.sound_button.is_active:
            return

        self.delete_error_message()
        if self.player.is_playing:
            self.stop_reproduction()
        else:
            self.player.play_morse(self.morse_box.toPlainText())
            self.sound_button.set_stop_style()


    def stop_reproduction(self):
        if not self.player.is_playing:
            return
        self.player.stop_playing()
        self.sound_button.set_play_style()
        self.check_morse_code()


    def on_player_finished(self):
        self.sound_button.set_play_style()
        self.check_morse_code()


if  __name__ == '__main__':
    app  = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
