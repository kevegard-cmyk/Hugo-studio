from PySide6.QtWidgets import QMessageBox


def show_myhugodesk_help(parent):
    QMessageBox.information(
        parent,
        "MyHugoDesk Help",
    )