import os
import random

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap, QMouseEvent, QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout

from audio import Audio
from settings_window import SettingsWindow
from shake import Shake

class MainWindow(QMainWindow):
    def __init__(self, settings):
        super().__init__()
        self.blinking_thread = None
        self.settings = settings
        self.cur_pict_index = 0
        self.pictures = []

        self.blink_timer = QtCore.QTimer()
        self.blink_timer.timeout.connect(self.check_blink)
        self.blinking = self.settings.get("blinking")
        self.blinking_rate = self.settings.get("blinking_rate")

        self.audio = Audio(self.settings)
        self.audio.volumeChanged.connect(self.on_volume_changed)
        self.initUI()
        self.audio.highVolume.connect(lambda v: self.shake.start() if v else self.shake.stop())
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
        self.shake = Shake(self.label, self.settings)
        self.reload_settings()
        self.label.setPixmap(self.pictures[0])
        self.label.setMouseTracking(True)

        self.tip_label = QLabel("Нажмите ЛКМ с зажатым shift для открытия настроек,"
                                "\nили зажатым ctrl для выхода")
        self.tip_label.setFixedSize(350, 30)
        self.tip_label.setStyleSheet("color: white")
        self.tip_label.setAlignment(Qt.AlignCenter)
        self.tip_label.hide()

        layout.addWidget(self.label, alignment=Qt.AlignCenter | Qt.AlignTop)
        layout.addWidget(self.tip_label, alignment=Qt.AlignCenter | Qt.AlignBottom)
        self.setCentralWidget(central_widget)
        self.label.installEventFilter(self)

    def start_blinking(self):
        self.blink_timer.stop()
        if self.blinking:
            self.blink_timer.start(int(self.blinking_rate * 1000))

    def check_blink(self):
        if not self.blinking:
            return
        rand = random.randint(0, 6)
        if rand == 1:
            if self.cur_pict_index == 0:
                self.label.setPixmap(QPixmap(self.pictures[2]))
                QtCore.QTimer.singleShot(200, lambda: self.label.setPixmap(QPixmap(self.pictures[0])))
            else:
                self.label.setPixmap(QPixmap(self.pictures[3]))
                QtCore.QTimer.singleShot(200, lambda: self.label.setPixmap(QPixmap(self.pictures[1])))

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
        if obj is self.label:
            if event.type() == QEvent.MouseButtonPress:
                if event.button() == Qt.LeftButton:
                    if event.modifiers() & Qt.ShiftModifier:
                        self.open_settings()
                        return True
                    if event.modifiers() & Qt.ControlModifier:
                        self.close_program()
                        return True

            elif event.type() == QEvent.Enter:
                self.tip_label.show()
            elif event.type() == QEvent.Leave:
                self.tip_label.hide()

        return super().eventFilter(obj, event)

    def open_settings(self):
        self.settings_window.show()

    def reload_settings(self):
        self.blinking = self.settings.get("blinking")
        self.blinking_rate = self.settings.get("blinking_rate")
        self.start_blinking()

        new_pictures = [
            self.settings.get("pict_silens_open_eye"),
            self.settings.get("pict_tall_open_eye"),
            self.settings.get("pict_silens_close_eye"),
            self.settings.get("pict_tall_close_eye")]
        self.pictures = [
            QPixmap(path if path and os.path.exists(path) else "pict_placeholder.png").scaledToWidth(300)
            for path in new_pictures
        ]
        self.update_picture()

        self.audio.update_threshold()

        self.shake.update_setting()

    def close_program(self):
        self.audio.stop()
        self.shake.stop()
        self.settings_window.hide()
        self.close()
