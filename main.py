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
