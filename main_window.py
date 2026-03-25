from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QStatusBar
from audio import Audio

class MainWindow(QMainWindow):
    def __init__(self, pictures):
        super().__init__()
        self.pictures = pictures
        self.cur_pict_index = 0
        self.pixmap_tall = QPixmap('pict_placeholder.png').scaledToWidth(300)
        self.pixmap_silence = QPixmap('pict_placeholder.png').scaledToWidth(300)

        self.audio = Audio(volume_threshold=500, check_interval=50)
        self.audio.volumeChanged.connect(self.on_volume_changed)

        self.initUI()
        self.audio.start()

    def initUI(self):
        self.setWindowTitle('PngTuber')
        self.setFixedSize(350, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 20, 0, 0)

        self.label = QLabel()
        if len(self.pictures) != 0:
            self.pixmap_tall, self.pixmap_silence = QPixmap(self.pictures[0]).scaledToWidth(300), QPixmap(self.pictures[1]).scaledToWidth(300)

        self.label.setPixmap(self.pixmap_tall)

        layout.addWidget(self.label, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.setCentralWidget(central_widget)

    def on_volume_changed(self, is_speaking):
        self.cur_pict_index = 1 if is_speaking else 0
        self.update_picture()

    def update_picture(self):
        if self.cur_pict_index == 0:
            self.label.setPixmap(QPixmap(self.pixmap_tall))
        else:
            self.label.setPixmap(QPixmap(self.pixmap_silence))

    def closeEvent(self, event):
        self.audio.stop()
        event.accept()