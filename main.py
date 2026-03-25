import sys
from PyQt5.QtWidgets import QApplication
from main_window import MainWindow

if __name__ == '__main__':
    App = QApplication(sys.argv)
    window = MainWindow(['комарка_молчит.png', 'комарка_не_молчит.png'])
    window.show()
    sys.exit(App.exec_())
