import random
import time

from PyQt5 import QtCore
import threading
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap, QMouseEvent, QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout
from audio import Audio
from settings_window import SettingsWindow
from settings_json import Settings

class MainWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.cur_pict_index = 0
        self.pictures = []

        self.blinking = self.settings.get("blinking")
        self.blinking_rate = self.settings.get("blinking_rate")
        self.blinking_thread = threading.Thread(target=self.blink_loop, daemon=True)
        self.blinking_thread.start()

        self.audio = Audio(volume_threshold=500, check_interval=50)
        self.audio.volumeChanged.connect(self.on_volume_changed)

        self.initUI()
        self.audio.start()

        self.settings_window = SettingsWindow(self.settings)
        self.settings_window.settingSaved.connect(self.reload_settings)

    def initUI(self):
        self.setWindowTitle('PngTuber')
        self.setFixedSize(350, 380)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 20, 0, 0)

        self.label = QLabel()
        self.reload_settings()
        self.label.setPixmap(self.pictures[0])
        self.label.setMouseTracking(True)

        self.tip_label = QLabel("Нажмите ЛКМ с зажатым alt для открытия настроек,\nили зажатым ctrl для выхода")
        self.tip_label.setFixedSize(350, 30)
        self.tip_label.setStyleSheet("color: white")
        self.tip_label.setAlignment(Qt.AlignCenter)
        self.tip_label.hide()

        layout.addWidget(self.label, alignment=Qt.AlignCenter | Qt.AlignTop)
        layout.addWidget(self.tip_label, alignment=Qt.AlignCenter | Qt.AlignBottom)
        self.setCentralWidget(central_widget)
        self.label.installEventFilter(self)

    def blink_loop(self):
        rand = random.randint(0, 6)
        if rand == 1 and self.blinking:
            if self.cur_pict_index == 0:
                self.label.setPixmap(QPixmap(self.pictures[2]))
            else:
                self.label.setPixmap(QPixmap(self.pictures[3]))
            time.sleep(0.2)
            if self.cur_pict_index == 0:
                self.label.setPixmap(QPixmap(self.pictures[0]))
            else:
                self.label.setPixmap(QPixmap(self.pictures[1]))
        time.sleep(self.blinking_rate)
        self.blink_loop()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()

    def on_volume_changed(self, is_speaking):
        self.cur_pict_index = 1 if is_speaking else 0
        self.update_picture()

    def update_picture(self):
        if self.cur_pict_index == 0:
            self.label.setPixmap(QPixmap(self.pictures[0]))
        else:
            self.label.setPixmap(QPixmap(self.pictures[1]))

    def eventFilter(self, obj, event):
        try:
            if obj == self.label:
                if event.type() == QEvent.MouseButtonPress:
                    mouse_event = QMouseEvent(event)
                    if mouse_event.buttons() == Qt.LeftButton \
                            and mouse_event.modifiers() & Qt.AltModifier:
                                self.open_settings()
                    if mouse_event.buttons() == Qt.LeftButton \
                            and mouse_event.modifiers() & Qt.ControlModifier:
                                self.close_program()
            if obj == self.label:
                if event.type() == QEvent.Enter:
                    self.tip_label.show()
            if obj == self.label:
                if event.type() == QEvent.Leave:
                    self.tip_label.hide()
            return False
        except Exception as e:
            print(e)

    def open_settings(self):
        self.settings_window.show()

    def reload_settings(self):
        self.blinking = self.settings.get("blinking")
        self.blinking_rate = self.settings.get("blinking_rate")
        new_pictures = [
            self.settings.get("pict_silens_open_eye"),
            self.settings.get("pict_tall_open_eye"),
            self.settings.get("pict_silens_close_eye"),
            self.settings.get("pict_tall_close_eye")]
        self.pictures = [QPixmap(i if i else "pict_placeholder.png").scaledToWidth(300) for i in new_pictures]
        self.update_picture()

    def close_program(self):
        self.audio.stop()
        self.blinking_thread = None
        self.close()
