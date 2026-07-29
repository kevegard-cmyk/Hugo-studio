from PySide6.QtWidgets import QDialog




from ui.dialogs.theme_install_dialog import ThemeInstallDialog


def install_theme(window):
    dialog = ThemeInstallDialog(window)
    dialog.exec()