from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)


class InstallationDialog(QDialog):

    def __init__(self, result, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Welcome to MyHugoDesk")
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel(
            "Hugo is required to create, preview, and build Hugo websites.\n"
            "Git is recommended for advanced features, such as theme installation and site deployment using Git. MyHugoDesk can be used without Git, but these features will not be available."
        ))

        hugo = "✓ Installed" if result["hugo"] else "✗ Not installed"
        git = "✓ Installed" if result["git"] else "✗ Not installed"

        layout.addWidget(QLabel(f"Hugo: {hugo}"))
        layout.addWidget(QLabel(f"Git:   {git}"))

        layout.addSpacing(15)

        buttons = QHBoxLayout()

        hugo_button = QPushButton("Download Hugo")
        hugo_button.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://gohugo.io/installation/")
            )
        )

        git_button = QPushButton("Download Git")
        git_button.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("https://git-scm.com/downloads")
            )
        )

        close_button = QPushButton("Continue")
        close_button.clicked.connect(self.accept)

        buttons.addWidget(hugo_button)
        buttons.addWidget(git_button)
        buttons.addStretch()
        buttons.addWidget(close_button)
        
        if result["hugo"]:
            hugo_button.setEnabled(False)

        if result["git"]:
            git_button.setEnabled(False)

        layout.addLayout(buttons)