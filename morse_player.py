import pygame
from PyQt6.QtCore import QObject, pyqtSignal, QTimer


class MorsePlayer(QObject):
    something_changed = pyqtSignal()
    highlight_changed = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.is_playing = False
        self.symbols = []
        self.currentIndex = 0

        pygame.mixer.init()
        self.dot_sound = pygame.mixer.Sound("assets/sounds/dot.wav")
        self.dash_sound = pygame.mixer.Sound("assets/sounds/dash.wav")


    def play(self, morse_code: str):
        self.is_playing = True
        self.symbols = morse_code.replace("\n", "/")
        self.highlight_changed.emit(self.currentIndex)
        self.something_changed.emit()
        self._play_morse_step()


    def _play_morse_step(self):
        if self.currentIndex >= len(self.symbols):
            self.is_playing = False
            self.currentIndex = 0
            self.highlight_changed.emit(-1)
            self.something_changed.emit()
            return

        if not self.is_playing:
            self.highlight_changed.emit(self.currentIndex)
            self.something_changed.emit()
            return

        symbol = self.symbols[self.currentIndex]
        if symbol == '.':
            self.dot_sound.play()
            delay = 200
        elif symbol == "-":
            self.dash_sound.play()
            delay = 400
        elif symbol == " ":
            delay = 200
        elif symbol == "/":
            delay = 600
        else:
            self.is_playing = False
            self.highlight_changed.emit(-1)
            self.something_changed.emit()
            return

        self.highlight_changed.emit(self.currentIndex)
        self.currentIndex += 1
        self.something_changed.emit()

        QTimer.singleShot(delay, lambda: self._play_morse_step())


    def pause(self):
        self.is_playing = False
        pygame.mixer.stop()
        self.highlight_changed.emit(self.currentIndex)
        self.something_changed.emit()


    def stop(self):
        self.is_playing = False
        pygame.mixer.stop()

        self.currentIndex = 0
        self.symbols = []

        self.highlight_changed.emit(-1)
        self.something_changed.emit()
