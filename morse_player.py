import pygame
from PyQt6.QtCore import QObject, pyqtSignal, QTimer


class MorsePlayer(QObject):
    finished_reproduction = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.is_playing = False
        self.dot_sound = None
        self.dash_sound = None
        self.on_finished_callback = None


    def play_morse(self, morse_code: str):
        self.is_playing = True

        morse_code = morse_code.replace("\n", "/")

        pygame.mixer.init()
        self.dot_sound = pygame.mixer.Sound("assets/sounds/dot.wav")
        self.dash_sound = pygame.mixer.Sound("assets/sounds/dash.wav")

        self._play_morse_step(morse_code, 0)


    def _play_morse_step(self, morse_code: str, index: int):
        if not self.is_playing or index >= len(morse_code):
            self.is_playing = False
            self.finished_reproduction.emit()
            return

        symbol = morse_code[index]
        if symbol == '.':
            self.dot_sound.play()
        elif symbol == "-":
            self.dash_sound.play()
        elif symbol == " ":
            pass
        elif symbol == "/":
            pass

        QTimer.singleShot(300, lambda: self._play_morse_step(morse_code, index + 1))


    def stop_playing(self):
        self.is_playing = False
        pygame.mixer.stop()
