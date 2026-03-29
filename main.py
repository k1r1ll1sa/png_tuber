import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
from settings_json import Settings

if __name__ == '__main__':
    App = QApplication(sys.argv)
    settings = Settings()
    window = MainWindow(settings)
    window.show()
    sys.exit(App.exec_())

#['комарка_молчит.png', 'комарка_не_молчит.png', 'комарка_молчит_глаза_закрыты.png', 'комарка_не_молчит_глаза_закрыты.png']