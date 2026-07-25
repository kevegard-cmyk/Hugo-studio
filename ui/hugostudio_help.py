from PySide6.QtWidgets import QMessageBox


def show_hugostudio_help(parent):
    QMessageBox.information(
        parent,
        "HugoStudio Help",
    )