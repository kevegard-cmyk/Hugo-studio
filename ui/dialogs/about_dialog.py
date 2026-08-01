from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QApplication,
)

from PySide6.QtCore import Qt

from core.version import APP_NAME, VERSION, RELEASE


class AboutDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle(f"About {APP_NAME}")
        self.setMinimumWidth(450)

        layout = QVBoxLayout(self)

        title = QLabel(f"<h2>{APP_NAME}</h2>")
        title.setAlignment(Qt.AlignCenter)

        version = QLabel(f"Version {VERSION} {RELEASE}")
        version.setAlignment(Qt.AlignCenter)

        description = QLabel(
            "A desktop IDE for Hugo websites.\n\n"
            "MyHugoDesk simplifies creating, editing, previewing "
            "and building Hugo websites while helping users "
            "understand how Hugo works."
        )
        description.setWordWrap(True)
        description.setAlignment(Qt.AlignCenter)

        built = QLabel(
            "Built with\n\n"
            "Python\n"
            "PySide6 (Qt)\n"
            "Hugo"
        )
        built.setAlignment(Qt.AlignCenter)

        copyright = QLabel(
            "2026"
        )
        copyright.setAlignment(Qt.AlignCenter)

        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(ok_button)

        layout.addWidget(title)
        layout.addWidget(version)
        layout.addSpacing(15)
        layout.addWidget(description)
        layout.addSpacing(15)
        layout.addWidget(built)
        layout.addStretch()
        layout.addWidget(copyright)
        layout.addSpacing(15)
        layout.addLayout(button_layout)