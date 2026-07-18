
import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from core.version import APP_NAME, VERSION, ORGANIZATION


def main():
    app = QApplication(sys.argv)

    app.setApplicationName(APP_NAME)
    app.setApplicationVersion(VERSION)
    app.setOrganizationName(ORGANIZATION)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()