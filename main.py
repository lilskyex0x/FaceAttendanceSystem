import sys
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow
from view.styles import NEON_STYLE


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(NEON_STYLE)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
