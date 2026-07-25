

from pathlib import Path

from PySide6.QtWidgets import QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QKeySequence

from ui.document_editor import DocumentEditor
from ui.icon import icon


EDITABLE_EXTENSIONS = {
    ".md",
    ".markdown",
    ".html",
    ".css",
    ".scss",
    ".sass",
    ".js",
    ".ts",
    ".toml",
    ".yaml",
    ".yml",
    ".json",
    ".xml",
    ".txt",
    ".csv",
}

def is_editable_file(path: Path) -> bool:
    return path.suffix.lower() in EDITABLE_EXTENSIONS


def create_editor(window):

    editor = DocumentEditor()

    window.update_editor_font(editor)
    editor.textChanged.connect(lambda: document_changed(window))

    return editor


def load_file(window, path):
    
   

    editor = create_editor(window)

    editor.file_path = path

    editor.blockSignals(True)

    editor.setPlainText(
        path.read_text(
            encoding="utf8",
            errors="ignore",
        )
    )

    editor.blockSignals(False)

    editor.setReadOnly(False)
    editor.modified = False

     # load_file()
    window.save_action.setEnabled(True)
    window.save_as_action.setEnabled(True)

    index = window.tabs.addTab(
        editor,
        path.name,
    )

    window.tabs.setCurrentIndex(index)
    editor.setFocus()

    window.write("Opened " + path.name)

    window.update_status()


def save(window):

    editor = current_editor(window)

    if editor is None:
        return

    if editor.file_path is None:
        return

    editor.file_path.write_text(
        editor.toPlainText(),
        encoding="utf8",
    )

    editor.modified = False

    window.tabs.setTabText(
        window.tabs.currentIndex(),
        editor.file_path.name,
    )

    window.write(f"Saved {editor.file_path.name}")

    window.update_status()


def document_changed(window):

    editor = current_editor(window)

    if editor is None:
        return

    if editor.isReadOnly():
        return

    if editor.modified:
        return

    editor.modified = True

    if editor.file_path:

        window.tabs.setTabText(
            window.tabs.currentIndex(),
            editor.file_path.name + " *",
        )

    window.update_status()


def close_tab(window, index):

    widget = window.tabs.widget(index)

    if widget == window.welcome:
        window.tabs.removeTab(index)
        widget.deleteLater()
        return

    window.tabs.setCurrentIndex(index)

    if not window.maybe_save():
        return

    window.tabs.removeTab(index)

    widget.deleteLater()
    if current_editor(window) is None:
        window.save_action.setEnabled(False)
        window.save_as_action.setEnabled(False)

    window.update_status()


def current_editor(window):

    widget = window.tabs.currentWidget()

    if isinstance(widget, DocumentEditor):
        return widget

    return None


def current_file(window):

    editor = current_editor(window)

    if editor:
        return editor.file_path

    return None
    
    
def is_file_open(window, path):
    for i in range(window.tabs.count()):
        widget = window.tabs.widget(i)

        if (
            isinstance(widget, DocumentEditor)
            and widget.file_path == path
        ):
            return True

    return False
    
def save_as(window):
    editor = current_editor(window)

    if editor is None:
        return

    filename, _ = QFileDialog.getSaveFileName(
        window,
        "Save As",
        str(editor.file_path) if editor.file_path else "",
        "Markdown (*.md);;All Files (*)",
    )

    if not filename:
        return

    editor.file_path = Path(filename)

    save(window)
    
def create_editor_actions(window):
    save_action = QAction(icon("save"), "Save", window)
    save_action.setShortcut(QKeySequence.StandardKey.Save)
    save_action.setShortcutContext(Qt.WindowShortcut)
    save_action.setToolTip("Save (Ctrl+S)")
    save_action.setEnabled(False)
    save_action.triggered.connect(lambda: save(window))

    # Keeps Ctrl+S active even though Save is not in a menu.
    window.addAction(save_action)

    save_as_action = QAction(icon("save-plus"), "Save As…", window)
    save_as_action.setToolTip("Save As…")
    save_as_action.setEnabled(False)
    save_as_action.triggered.connect(lambda: save_as(window))

    return save_action, save_as_action