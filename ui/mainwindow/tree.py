import shutil
from pathlib import Path




    
from PySide6.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QMenu,
    QMessageBox,
    QLineEdit,
)
    

from ui.document_editor import DocumentEditor
from ui.mainwindow.editor import load_file

def is_single_path_component(name):
    """Return whether *name* can only name an item in its current folder."""
    candidate = Path(name)

    return (
        bool(name)
        and name not in {".", ".."}
        and not candidate.is_absolute()
        and len(candidate.parts) == 1
        and candidate.name == name
    )


def is_inside_project(window, path):
    """Return whether the resolved path is contained by the open project."""
    try:
        path.resolve().relative_to(Path(window.project).resolve())
    except ValueError:
        return False

    return True


def validate_destination(window, name, destination):
    if is_single_path_component(name) and is_inside_project(window, destination):
        return True

    QMessageBox.warning(
        window,
        "Invalid name",
        "Names cannot contain folders, absolute paths, '.' or '..'.",
    )
    return False


def has_open_file_in_item(window, path):
    return any(
        isinstance(widget, DocumentEditor)
        and widget.file_path is not None
        and (
            widget.file_path == path
            or (path.is_dir() and path in widget.file_path.parents)
        )
        for index in range(window.tabs.count())
        for widget in [window.tabs.widget(index)]
    )


def show_context_menu(window, position):

    index = window.tree.indexAt(position)

    if not index.isValid():
        return

    path = Path(window.model.filePath(index))

    menu = QMenu(window)

    new_post = menu.addAction("New Page/Post…")
    new_file = menu.addAction("New File…")
    new_folder = menu.addAction("New Folder")
    insert_images_action = menu.addAction("Insert Images...")
    menu.addSeparator()

    rename = menu.addAction("Rename")
    delete = menu.addAction("Delete")

    action = menu.exec(
        window.tree.viewport().mapToGlobal(position)
    )

    if action == new_post:
        create_post(window, path)
        
    elif action == new_file:
        new_file_item(window, path)

    elif action == new_folder:
        new_folder_item(window, path)
        
    elif action == insert_images_action:
        insert_images(window, path)

    elif action == rename:
        rename_item(window, path)

    elif action == delete:
        delete_item(window, path)


def create_post(window, path):
    
    

    if path.is_file():
        folder = path.parent
    else:
        folder = path

    content_root = window.project / "content"
    if folder == window.project:
        folder = content_root

    try:
        relative_folder = folder.resolve().relative_to(
            content_root.resolve()
        )
    except ValueError:
        QMessageBox.warning(
            window,
            "Select a Content Folder",
            "New Hugo content must be created inside the content folder.",
        )
        return

    title, ok = QInputDialog.getText(
        window,
        "New Page/Post",
        "File name (.md is added automatically):",
    )

    if not ok or not title:
        return

    slug = title.lower().replace(" ", "-")
    if (
        not slug
        or Path(slug).is_absolute()
        or len(Path(slug).parts) != 1
        or slug in {".", ".."}
    ):
        QMessageBox.warning(
            window,
            "Invalid Post Title",
            "Enter a title that does not contain a path.",
        )
        return

    content_path = relative_folder / f"{slug}.md"
    file = content_root / content_path

    if file.exists():
        QMessageBox.warning(
            window,
            "File exists",
            f"{file.name} already exists."
        )
        return

    if not window.hugo.new_content(window.project, content_path):
        QMessageBox.critical(
            window,
            "Post Creation Failed",
            "Hugo could not create the new post.",
        )
        return

    refresh_tree(window)
    load_file(window, file)

    window.write(f"Created page {file.name}")



def refresh_tree(window):

    if not window.project:
        return

    window.model.setRootPath("")

    index = window.model.setRootPath(
        str(window.project)
    )

    window.tree.setRootIndex(index)
    for column in range(1, window.model.columnCount()):
        window.tree.hideColumn(column)


def new_folder_item(window, path):

    folder = path.parent if path.is_file() else path

    name, ok = QInputDialog.getText(
        window,
        "New Folder",
        "Folder name",
    )

    if not ok or not name.strip():
        return

    name = name.strip()
    folder_path = folder / name

    if not validate_destination(window, name, folder_path):
        return

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
    if has_open_file_in_item(window, path):
        QMessageBox.warning(
            window,
            "File is open",
            "Close any open files in this item before deleting it.",
        )
        return

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

    refresh_tree(window)
    window.write(f"Deleted {path.name}")


def rename_item(window, path):
    
    if has_open_file_in_item(window, path):
        QMessageBox.warning(
            window,
            "File is open",
            "Close the file before renaming, moving or deleting it."
        )
        return

    name, ok = QInputDialog.getText(
        window,
        "Rename",
        "New name:",
        text=path.name,
    )

    if not ok or not name.strip():
        return

    name = name.strip()

    if path.is_file() and not Path(name).suffix:
        name += path.suffix

    new_path = path.parent / name

    if not validate_destination(window, name, new_path):
        return

    if new_path.exists():
        QMessageBox.warning(
            window,
            "Already exists",
            f"{name} already exists."
        )
        return

    try:
        path.rename(new_path)
    except OSError as error:
        QMessageBox.critical(
            window,
            "Rename Failed",
            str(error),
        )
        return

    refresh_tree(window)

    window.write(f"Renamed {path.name} → {new_path.name}")
    
    
    
    
def insert_images(window, path):

    if path.is_file():
        path = path.parent

    files, _ = QFileDialog.getOpenFileNames(
        window,
        "Select Images",
        "",
        "Images (*.png *.jpg *.jpeg *.gif *.bmp *.webp)"
    )

    if not files:
        return

    for file in files:
        src = Path(file)
        dst = path / src.name

        if dst.exists():

            msg = QMessageBox(window)
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("File already exists")
            msg.setText(f"'{dst.name}' already exists.")
            msg.setInformativeText(
                "Do you want to replace the existing file?"
            )

            overwrite = msg.addButton(
                "Overwrite",
                QMessageBox.AcceptRole
            )
            skip = msg.addButton(
                "Skip",
                QMessageBox.RejectRole
            )
            cancel = msg.addButton(
                "Cancel",
                QMessageBox.DestructiveRole
            )

            msg.exec()

            if msg.clickedButton() == cancel:
                return

            if msg.clickedButton() == skip:
                continue

            # Overwrite selected

        shutil.copy2(src, dst)

    refresh_tree(window)



def new_file_item(window, path):
    folder = path.parent if path.is_file() else path

    name, ok = QInputDialog.getText(
        window,
        "New File",
        "File name:",
    )

    if not ok:
        return

    filename = name.strip()

    if not filename:
        return

    file_path = folder / filename

    if not validate_destination(window, filename, file_path):
        return

    if file_path.exists():
        QMessageBox.warning(
            window,
            "File Exists",
            f"{filename} already exists.",
        )
        return

    try:
        file_path.touch()
    except OSError as error:
        QMessageBox.critical(
            window,
            "File Creation Failed",
            str(error),
        )
        return
        
        
    refresh_tree(window)

    load_file(window, file_path)

    window.write(f"Created file {file_path.name}")

