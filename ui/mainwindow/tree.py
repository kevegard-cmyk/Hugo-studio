import datetime
import shutil

from pathlib import Path
from textwrap import dedent

from PySide6.QtWidgets import (
    QInputDialog,
    QMessageBox,
    QMenu,
)


def show_context_menu(window, position):

    index = window.tree.indexAt(position)

    if not index.isValid():
        return

    path = Path(window.model.filePath(index))

    menu = QMenu(window)

    new_post = menu.addAction("New Post")
    new_folder = menu.addAction("New Folder")

    menu.addSeparator()

    rename = menu.addAction("Rename")
    delete = menu.addAction("Delete")

    action = menu.exec(
        window.tree.viewport().mapToGlobal(position)
    )

    if action == new_post:
        create_post(window, path)

    elif action == new_folder:
        new_folder_item(window, path)

    elif action == rename:
        rename_item(window, path)

    elif action == delete:
        delete_item(window, path)


def create_post(window, path):

    if path.is_file():
        folder = path.parent
    else:
        folder = path

    title, ok = QInputDialog.getText(
        window,
        "New Post",
        "Post title",
    )

    if not ok or not title:
        return

    slug = title.lower().replace(" ", "-")

    file = folder / f"{slug}.md"

    if file.exists():
        QMessageBox.warning(
            window,
            "File exists",
            f"{file.name} already exists."
        )
        return

    file.write_text(
        dedent(f"""\
        ---
        title: "{title}"
        date: {datetime.date.today()}
        tags: []
        draft: false
        ---

        # {title}
        """),
        encoding="utf8",
    )

    refresh_tree(window)

    window.write(f"Created {file}")


def refresh_tree(window):

    if not window.project:
        return

    window.model.setRootPath("")

    index = window.model.setRootPath(
        str(window.project)
    )

    window.tree.setRootIndex(index)


def new_folder_item(window, path):

    folder = path.parent if path.is_file() else path

    name, ok = QInputDialog.getText(
        window,
        "New Folder",
        "Folder name",
    )

    if not ok or not name:
        return

    folder_path = folder / name

    if folder_path.exists():
        QMessageBox.warning(
            window,
            "Folder exists",
            f"{folder_path.name} already exists."
        )
        return

    folder_path.mkdir()

    refresh_tree(window)

    window.write(f"Created folder {folder_path.name}")


def delete_item(window, path):

    answer = QMessageBox.question(
        window,
        "Delete",
        f"Delete '{path.name}'?",
        QMessageBox.Yes | QMessageBox.No,
    )

    if answer != QMessageBox.Yes:
        return

    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()

    editor = window.current_editor()

    if (
        editor is not None
        and editor.file_path is not None
        and editor.file_path == path
    ):
        window.close_tab(window.tabs.currentIndex())

    refresh_tree(window)

    window.write(f"Deleted {path.name}")


def rename_item(window, path):

    name, ok = QInputDialog.getText(
        window,
        "Rename",
        "New name:",
        text=path.name,
    )

    if not ok or not name:
        return

    if path.is_file() and not Path(name).suffix:
        name += path.suffix

    new_path = path.parent / name

    if new_path.exists():
        QMessageBox.warning(
            window,
            "Already exists",
            f"{name} already exists."
        )
        return

    path.rename(new_path)

    refresh_tree(window)

    window.write(f"Renamed {path.name} → {new_path.name}")