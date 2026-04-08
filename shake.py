import random

from PyQt5.QtCore import QObject, QTimer


class Shake(QObject):
    def __init__(self, target_widget, settings, duration=800):
        super().__init__(target_widget)
        self.settings = settings
        self.target = target_widget
        self.shaking = self.settings.get('shaking')
        self.shaking_intensity = self.settings.get('shaking_intensity', 5)
        self.duration = duration

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._apply_shake)
        self.timer.setInterval(20)

        self.elapsed = 0
        self.original_pos = None

    def start(self):
        if self.timer.isActive():
            return
        self.original_pos = self.target.pos()
        self.elapsed = 0
        self.timer.start()

    def stop(self):
        if self.timer.isActive():
            self.timer.stop()
            if self.original_pos is not None:
                self.target.move(self.original_pos)

    def _apply_shake(self):
        self.elapsed += 20
        if self.elapsed >= self.duration:
            self.stop()
            return
        if self.shaking:
            damping = 1.0 - self.elapsed / self.duration
            dx = int(random.uniform(-1, 1) * self.shaking_intensity * damping)
            dy = int(random.uniform(-0.6, 0.6) * self.shaking_intensity * damping)

            new_x = int(self.original_pos.x() + dx)
            new_y = int(self.original_pos.y() + dy)
            self.target.move(new_x, new_y)
        else:
            return

    def update_setting(self):
        self.shaking_intensity = self.settings.get('shaking_intensity', 5)
        self.shaking = self.settings.get('shaking')