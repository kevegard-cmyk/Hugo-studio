from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QInputDialog,
    QMessageBox,
)
         
            
def new_project(window):

    if not window.maybe_save():
        return

    name, ok = QInputDialog.getText(
        window,
        "New Project",
        "Project name:",
    )

    if not ok or not name.strip():
        return

    name = name.strip()

    workspace = QFileDialog.getExistingDirectory(
        window,
        "Select Workspace",
    )

    if not workspace:
        return

    project = Path(workspace) / name

    if project.exists():

        QMessageBox.warning(
            window,
            "Project Exists",
            f"{project}\n\nChoose another project name.",
        )
        return

    window.reset_editor()

    if window.hugo.new_project(workspace, name):
       load_project(window, project)
    else:
        
        QMessageBox.critical(
            window,
            "Project Creation Failed",
            "Hugo Studio could not create the project.\n\nCheck the log for details.",
        )
 
    
         
def load_project(window, folder):

    folder = Path(folder)

    if not folder.exists():

        QMessageBox.warning(
            window,
            "Missing Project",
            f"{folder}\n\nProject no longer exists."
        )

        return False

    window.project = folder

    index = window.model.setRootPath(str(folder))

    window.tree.setModel(window.model)
    window.tree.setRootIndex(index)

    window.settings.last_project = str(folder)
    window.settings.add_recent_project(str(folder))
    window.settings.save()

    update_recent_projects_menu(window)

    window.write(f"Opened {folder}")

    window.update_status()

    return True
    

def restore_last_project(window):

    folder = window.settings.last_project

    if not folder:
        return

    window.reset_editor()

    load_project(window, folder)
    
def open_project(window):

    if not window.maybe_save():
        return

    window.reset_editor()

    folder = QFileDialog.getExistingDirectory(
        window,
        "Project",
    )

    if not folder:
        return

    load_project(window, folder)
    
def update_recent_projects_menu(window):

    window.recent_menu.clear()

    recent = window.settings.recent_projects

    if not recent:

        action = QAction("(Empty)", window)
        action.setEnabled(False)
        window.recent_menu.addAction(action)
        return

    for folder in recent:

        action = QAction(folder, window)

        action.triggered.connect(
            lambda checked=False, p=folder:
                open_recent_project(window, p)
        )

        window.recent_menu.addAction(action)
        
def open_recent_project(window, folder):

    if not window.maybe_save():
        return

    window.reset_editor()

    load_project(window, folder)
    
    
    