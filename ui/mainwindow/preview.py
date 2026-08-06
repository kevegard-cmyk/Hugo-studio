from PySide6.QtWidgets import QDialog

from ui.dialogs.preview_dialog import PreviewDialog


# def preview(window):

    # if window.project is None:
        # return

    # dialog = PreviewDialog(
        # parent=window,
        # settings=window.settings,
    # )

    # if dialog.exec() != QDialog.DialogCode.Accepted:
        # return

    # options = dialog.options()

    # window.hugo.preview(
        # window.project,
        # options,
    # )
    
    
def preview(window):

    if window.project is None:
        return

    if window.hugo.server_running:

        if window.hugo.open_browser:
            import webbrowser
            webbrowser.open(window.hugo.server_url)

        return

    options = window.settings.get_group("preview")

    window.hugo.preview(
        window.project,
        options,
    )
    
    
def preview_settings(window):

    if window.project is None:
        return

    dialog = PreviewDialog(
        parent=window,
        settings=window.settings,
        server_running=window.hugo.server_running,
        server_url=window.hugo.server_url,
    )

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return

    options = dialog.options()

    window.hugo.preview(
        window.project,
        options,
    )