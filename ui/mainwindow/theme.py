from PySide6.QtWidgets import QDialog




from ui.dialogs.theme_install_dialog import ThemeInstallDialog


def install_theme(window):
    dialog = ThemeInstallDialog(
        parent=window,
        settings=window.settings,
    )

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return

    # later:
    # options = dialog.options()
    # window.hugo.install_theme(options)