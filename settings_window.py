from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit, QFileDialog, QWidget, \
    QGroupBox, QLineEdit, QCheckBox, QSpinBox, QSlider, QFrame


class SettingsWindow(QMainWindow):
    settingSaved = pyqtSignal()

    def __init__(self, settings):
        super().__init__()
        self.dragging = None
        self.title_bar_height = 70
        self.settings = settings
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Settings")
        self.setFixedSize(800, 600)
        self.setStyleSheet("background-color: #1F1F1F; color: white")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.installEventFilter(self)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # === Верхняя панель ===
        title_bar = QHBoxLayout()
        title_bar.setSpacing(10)

        title = QLabel("Настройки")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #FFFFFF")
        title.setAlignment(Qt.AlignLeft)
        title_bar.addWidget(title, stretch=1)

        # Кнопка сворачивания
        minimize_btn = QPushButton("─")
        minimize_btn.setFixedSize(30, 30)
        minimize_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D2D2D;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #4D4D4D;
            }
        """)
        minimize_btn.clicked.connect(self.showMinimized)
        title_bar.addWidget(minimize_btn)

        # Кнопка закрытия
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #2D2D2D;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #E74C3C;
            }
        """)
        close_btn.clicked.connect(self.close)
        title_bar.addWidget(close_btn)

        main_layout.addLayout(title_bar)

        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("background-color: #333;")
        separator.setFixedHeight(2)
        main_layout.addWidget(separator)

        # === Категория: открытые глаза ===
        group_open = QGroupBox("Открытые глаза")
        group_open.setStyleSheet("""
            QGroupBox { 
                border: 1px solid #333; 
                border-radius: 5px; 
                margin-top: 10px; 
                padding-top: 10px; 
                font-weight: bold
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
            }
        """)

        layout_open = QVBoxLayout(group_open)
        layout_open.setSpacing(10)

        row1 = self.create_image_row("Говорить (открытые глаза)", "pict_tall_open_eye")
        layout_open.addLayout(row1)

        row2 = self.create_image_row("Молчать (открытые глаза)", "pict_silens_open_eye")
        layout_open.addLayout(row2)

        main_layout.addWidget(group_open)

        # === Категория: закрытые глаза ===
        group_close = QGroupBox("Закрытые глаза")
        group_close.setStyleSheet("""
            QGroupBox { 
                border: 1px solid #333; 
                border-radius: 5px; 
                margin-top: 10px; 
                padding-top: 10px; 
                font-weight: bold
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
            }
        """)
        layout_close = QVBoxLayout(group_close)
        layout_close.setSpacing(10)

        row3 = self.create_image_row("Говорить (закрытые глаза)", "pict_tall_close_eye")
        layout_close.addLayout(row3)

        row4 = self.create_image_row("Молчать (закрытые глаза)", "pict_silens_close_eye")
        layout_close.addLayout(row4)

        # === Подкатегория: Моргание ===
        blink_row = QHBoxLayout()

        self.blink_checkbox = QCheckBox("Включить моргание")
        self.blink_checkbox.setChecked(self.settings.get("blinking"))
        blink_row.addWidget(self.blink_checkbox)

        blink_rate_label = QLabel("Частота моргания:")
        blink_row.addWidget(blink_rate_label)

        self.blink_rate_slider = QSlider(Qt.Horizontal)
        self.blink_rate_slider.setMinimum(1)
        self.blink_rate_slider.setMaximum(100)
        self.blink_rate_slider.setValue(int(self.settings.get("blinking_rate", 2)*10))
        self.blink_rate_slider.setFixedWidth(200)
        blink_row.addWidget(self.blink_rate_slider)

        self.blink_rate_value_lable = QLabel(f"{self.settings.get("blinking_rate")}")
        blink_row.addWidget(self.blink_rate_value_lable)

        self.blink_rate_slider.valueChanged.connect(lambda v: self.blink_rate_value_lable.setText(f"{v/10} сек"))

        layout_close.addLayout(blink_row)

        main_layout.addWidget(group_close)

        save_btn = QPushButton("Сохранить настройки")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_settings)
        main_layout.addWidget(save_btn)

        main_layout.addStretch()

    def create_image_row(self, label_text, setting_key):
        layout = QHBoxLayout()
        layout.setSpacing(10)

        label = QLabel(label_text)
        label.setStyleSheet("font-size: 12px; min-width: 200px")
        layout.addWidget(label)

        text_edit = QLineEdit()
        text_edit.setPlaceholderText("Путь к изображению...")
        text_edit.setStyleSheet("""
            QLineEdit {
                background-color: #2D2D2D;
                border: 1px solid #444;
                border-radius: 3px;
                color: white;
                padding: 5px; 
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        current_value = self.settings.get(setting_key, "")
        text_edit.setText(current_value)
        layout.text_edit = text_edit
        layout.setting_key = setting_key
        layout.addWidget(text_edit, stretch=1)

        btn = QPushButton("Выбрать файл")
        btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 5px 15px;
                border-radius: 3px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        btn.clicked.connect(lambda: self.browse_file(text_edit))
        layout.addWidget(btn)

        return layout

    def browse_file(self, text_edit):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Изображения (*.png *.jpg *.jpeg);;Все файлы (*)"
        )
        if file_path:
            text_edit.setText(file_path)

    def save_settings(self):
        central_widget = self.centralWidget()
        main_layout = central_widget.layout()

        for i in range(main_layout.count()):
            item = main_layout.itemAt(i)
            if item.widget() and isinstance(item.widget(), QGroupBox):
                group_box = item.widget()
                layout = group_box.layout()

                for j in range(layout.count()):
                    row_layout = layout.itemAt(j)
                    if hasattr(row_layout, 'text_edit') and hasattr(row_layout, 'setting_key'):
                        key = row_layout.setting_key
                        value = row_layout.text_edit.text().strip()
                        self.settings.set(key, value)

        self.settings.set("blinking", self.blink_checkbox.isChecked())
        self.settings.set("blinking_rate", self.blink_rate_slider.value()/10)
        self.settings.save()
        self.settingSaved.emit()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if event.y() < self.title_bar_height:
                self.dragging = True
                self.drag_start_position = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()
            else:
                self.dragging = False

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.dragging:
            self.move(event.globalPos() - self.drag_start_position)
            event.accept()