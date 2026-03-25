import random
import time

from PyQt5 import QtCore
import threading
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap, QMouseEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout
from audio import Audio

class MainWindow(QMainWindow):
    def __init__(self, pictures):
        super().__init__()
        self.pictures = pictures
        self.cur_pict_index = 0
        self.pixmap_tall = QPixmap('pict_placeholder.png').scaledToWidth(300)
        self.pixmap_silence = QPixmap('pict_placeholder.png').scaledToWidth(300)
        self.pixmap_tall_close_eyes = QPixmap('pict_placeholder.png').scaledToWidth(300)
        self.pixmap_silence_close_eyes = QPixmap('pict_placeholder.png').scaledToWidth(300)

        self.audio = Audio(volume_threshold=500, check_interval=50)
        self.audio.volumeChanged.connect(self.on_volume_changed)

        self.initUI()
        self.audio.start()
        self.blinking_thread = threading.Thread(target=self.blink_loop)
        self.blinking_thread.start()

    def initUI(self):
        self.setWindowTitle('PngTuber')
        self.setFixedSize(350, 350)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 20, 0, 0)

        self.label = QLabel()
        if len(self.pictures) != 0:
            self.pictures = [QPixmap(self.pictures[0]).scaledToWidth(300),
                             QPixmap(self.pictures[1]).scaledToWidth(300),
                             QPixmap(self.pictures[2]).scaledToWidth(300),
                             QPixmap(self.pictures[3]).scaledToWidth(300)]
        self.label.setPixmap(self.pictures[0])
        self.label.setMouseTracking(True)

        layout.addWidget(self.label, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.setCentralWidget(central_widget)
        self.label.installEventFilter(self)

    def blink_loop(self):
        rand = random.randint(0, 100)
        if rand >= 60:
            if self.cur_pict_index == 0:
                self.label.setPixmap(QPixmap(self.pictures[2]))
            else:
                self.label.setPixmap(QPixmap(self.pictures[3]))
            time.sleep(0.2)
            if self.cur_pict_index == 0:
                self.label.setPixmap(QPixmap(self.pictures[0]))
            else:
                self.label.setPixmap(QPixmap(self.pictures[1]))
        time.sleep(2)
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
                    if mouse_event.buttons() == Qt.LeftButton:
                        self.on_label_clicked()
            return False
        except Exception as e:
            print(e)

    def on_label_clicked(self):
        print('clicked')

    def closeEvent(self, event):
        self.audio.stop()
        event.accept()

