from pathlib import Path

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QMessageBox,
    QDialog,
)
         
from core.hugo_project import validate_hugo_project
from ui.dialogs.new_project_dialog import NewProjectDialog

            
def new_project(window):
    dialog = NewProjectDialog(window)

    if dialog.exec() != QDialog.DialogCode.Accepted:
        return

    options = dialog.options()
    project = options.parent_folder / options.name

    if project.exists():
        QMessageBox.warning(
            window,
            "Project Exists",
            f"{project}\n\nChoose another project name.",
        )
        return

    if not window.maybe_save_all():
        return

    if not window.hugo.new_project(options):
        QMessageBox.critical(
            window,
            "Project Creation Failed",
            "Hugo Studio could not create the project.\n\n"
            "Check the log for details.",
        )
        return

    window.reset_editor()
    load_project(window, project)
 
    
         
def load_project(window, folder):
    
    folder = Path(folder)

    is_valid, message = validate_hugo_project(folder)
    if not is_valid:
        QMessageBox.warning(
            window,
            "Invalid Hugo Project",
            f"{folder}\n\n{message}",
        )
        return False

    window.project = folder

    index = window.model.setRootPath(str(folder))

    window.tree.setModel(window.model)
    window.tree.setRootIndex(index)
    
    # Show only the Name column
    for column in range(1, window.model.columnCount()):
        window.tree.hideColumn(column)
    
    window.update_project_view()
    window.settings.last_project = str(folder)
    window.settings.add_recent_project(str(folder))
    window.settings.save()

    update_recent_projects_menu(window)

    window.write(f"Opened {folder}")
    

    window.update_window_title()
    window.update_status()
  
    return True
    

def restore_last_project(window):

    folder = window.settings.last_project

    if not folder:
        return

    window.reset_editor()

    load_project(window, folder)
    
def open_project(window):
    
    # if not window.maybe_save():
        # return
        
    if not window.maybe_save_all():
        return    

    
    
    

    folder = QFileDialog.getExistingDirectory(
        window,
        "Project",
    )


    if not folder:
        return
        
    window.reset_editor()
    load_project(window, folder)
    
def update_recent_projects_menu(window):

    window.recent_menu.clear()
    clear_action = QAction("Clear Recent Projects...", window)
    clear_action.triggered.connect(
        lambda: clear_recent_projects(window)
    )
    window.recent_menu.addAction(clear_action)
    window.recent_menu.addSeparator()

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

    if not window.maybe_save_all():
        return

    window.reset_editor()

    load_project(window, folder)
    
    
def clear_recent_projects(window):
    window.settings.recent_projects.clear()
    window.settings.last_project = ""

    window.settings.save()

    window.project = None
    window.reset_editor()
    window.update_window_title()
    window.update_status()

    update_recent_projects_menu(window)
    
def close_project(window):
    if window.project is None:
        return

    if not window.maybe_save_all():
        return

    window.hugo.stop_server()
    window.reset_editor()

    window.project = None
    window.settings.last_project = ""
    window.settings.save()

    window.update_project_view()
    window.update_window_title()
    window.update_status()

    window.write("Closed project.")
