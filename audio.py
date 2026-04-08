import time
import pyaudio
import numpy as np
import threading
from PyQt5.QtCore import QObject, pyqtSignal

class Audio(QObject):
    volumeChanged = pyqtSignal(bool)
    highVolume = pyqtSignal(bool)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.check_interval = 50.0 / 1000.0
        self.is_speaking = False

        self.shake_threshold = 1500
        self.volume_threshold = 750
        self.is_high_volume = False
        self.update_threshold()

        self.audio = None
        self.stream = None
        self.running = False
        self.thread = None

    def start(self):
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=1024)

            self.running = True
            self.thread = threading.Thread(target=self.monitor_loop, daemon=True)
            self.thread.start()
        except Exception as e:
            print(f'def start error: {e}')

    def monitor_loop(self):
        while self.running:
            self.check_volume()
            time.sleep(self.check_interval)

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
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
            is_cur_high = volume > self.shake_threshold

            if bool(is_speaking_now) != self.is_speaking:
                self.is_speaking = bool(is_speaking_now)
                self.volumeChanged.emit(self.is_speaking)

            if bool(is_cur_high) != self.is_high_volume:
                self.is_high_volume = bool(is_cur_high)
                self.highVolume.emit(bool(is_cur_high))

        except Exception as e:
            print(f'def check_volume error: {e}')

    def update_threshold(self):
        self.volume_threshold = self.settings.get("volume_threshold")
        self.shake_threshold = self.settings.get("shaking_threshold")