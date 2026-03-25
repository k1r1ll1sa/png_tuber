import pyaudio
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

class Audio(QObject):
    volumeChanged = pyqtSignal(bool)

    def __init__(self, volume_threshold=500, check_interval=50):
        super().__init__()
        self.volume_threshold = volume_threshold
        self.check_interval = check_interval
        self.is_speaking = False
        self.audio = None
        self.stream = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_volume)

    def start(self):
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024)
            self.timer.start(self.check_interval)
        except Exception as e:
            print(f'def start error: {e}')

    def stop(self):
        self.timer.stop()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        if self.audio:
            self.audio.terminate()

    def check_volume(self):
        try:
            data = np.frombuffer(self.stream.read(1024), dtype=np.int16)
            volume = np.abs(data).mean()
            is_speaking_now = volume > self.volume_threshold

            if bool(is_speaking_now) != self.is_speaking:
                self.is_speaking = bool(is_speaking_now)
                self.volumeChanged.emit(self.is_speaking)

        except Exception as e:
            print(f'def check_volume error: {e}')

    def set_threshold(self, threshold):
        self.volume_threshold = threshold