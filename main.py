
import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow




def main():
    app = QApplication(sys.argv)
    
    app.setApplicationName("Hugo Studio")
    app.setApplicationVersion("0.4.2")
    app.setOrganizationName("Hugo Studio")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()