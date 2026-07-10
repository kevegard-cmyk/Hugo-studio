from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton
from PySide6.QtCore import QProcess
from pathlib import Path
from textwrap import dedent
import datetime
import shutil
from authoring.markdown_actions import MarkdownActions
from ui.authoring_toolbar import AuthoringToolbar


from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QFileDialog,
    QFileSystemModel,
    QTreeView,
    QSplitter,
    QPlainTextEdit,
    QInputDialog,
    QMessageBox,
)

from utils.markdown_highlighter import MarkdownHighlighter
from ui.markdown_help import show_markdown_help
from core.hugo_service import HugoService
from core.settings import Settings


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.modified = False
        self.settings = Settings()
        self.editor_font_size = self.settings.editor_font_size
        self.project = None
        self.current = None

        self.hugo = HugoService(self)

        self.resize(1200, 700)
        self.setWindowTitle("Hugo Studio v0.4 Alpha")

        self.build_ui()

        self.restore_last_project()
        
        

    def build_ui(self):

        # ---------- Menu ----------

        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        hugo_menu = menu.addMenu("&Hugo")
        view_menu = menu.addMenu("&View")
        
        font_up = QAction("Increase Font Size", self)
        font_up.setShortcut("Ctrl++")
        font_up.triggered.connect(self.increase_font_size)
        view_menu.addAction(font_up)
        font_down = QAction("Decrease Font Size", self)
        font_down.setShortcut("Ctrl+-")
        font_down.triggered.connect(self.decrease_font_size)
        view_menu.addAction(font_down)
        font_reset = QAction("Reset Font Size", self)
        font_reset.setShortcut("Ctrl+0")
        font_reset.triggered.connect(self.reset_font_size)
        view_menu.addAction(font_reset)

        

        

        open_action = QAction("Open Project...", self)
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)

        self.recent_menu = file_menu.addMenu("Recent Projects")
        
        file_menu.addSeparator()
        
        self.save_action = file_menu.addAction("Save")
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save)
        self.save_action.setEnabled(False)
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        preview_action = QAction("Preview", self)
        preview_action.setShortcut("F5")
        preview_action.triggered.connect(self.preview)
        hugo_menu.addAction(preview_action)

        build_action = QAction("Build", self)
        build_action.setShortcut("F6")
        build_action.triggered.connect(self.build)
        hugo_menu.addAction(build_action)

        hugo_menu.addSeparator()
    
        help_action = QAction("Markdown Help", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self.md_help)
        hugo_menu.addAction(help_action)

     

        splitter = QSplitter()
        self.setCentralWidget(splitter)

        self.model = QFileSystemModel()

        self.tree = QTreeView()
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        self.tree.clicked.connect(self.open_file)

        splitter.addWidget(self.tree)

        right = QWidget()
        layout = QVBoxLayout(right)

        self.editor = QPlainTextEdit()
        self.editor.setReadOnly(True)
        self.editor.setPlaceholderText(
    "Open a Markdown file or create a new post."
        )
        MarkdownHighlighter(self.editor.document())
        self.update_editor_font()
        self.editor.textChanged.connect(self.document_changed)
        self.md = MarkdownActions(self.editor)
        self.authoring = AuthoringToolbar(self.md)

        layout.addWidget(self.authoring)
        layout.addWidget(self.editor)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(140)
        layout.addWidget(self.log)
        
        command_layout = QHBoxLayout()

        self.command = QLineEdit()
        self.command.setPlaceholderText("Enter command...")

        run_button = QPushButton("Run")

        command_layout.addWidget(self.command)
        command_layout.addWidget(run_button)

        layout.addLayout(command_layout)

        run_button.clicked.connect(self.run_command)
        self.command.returnPressed.connect(self.run_command)

        splitter.addWidget(right)
        splitter.setSizes([300, 900])
        self.update_recent_projects_menu()

    def write(self, message):
        self.log.appendPlainText(message)

    def restore_last_project(self):

        folder = self.settings.last_project

        if not folder:
            return

        folder = Path(folder)

        if not folder.exists():
            return

        self.project = folder

        index = self.model.setRootPath(str(folder))
        self.tree.setModel(self.model)
        self.tree.setRootIndex(index)

        self.write(f"Restored {folder}")

    def open_project(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Project",
        )

        if not folder:
            return

        self.project = Path(folder)

        index = self.model.setRootPath(folder)

        self.tree.setModel(self.model)
        self.tree.setRootIndex(index)

        self.settings.last_project = folder
        self.settings.add_recent_project(folder)
        self.settings.save()
        self.update_recent_projects_menu()
        self.write("Opened " + folder)

    def open_file(self, index):

        path = Path(self.model.filePath(index))

        if path.is_dir():
            return

        self.current = path

        self.editor.setPlainText(
            path.read_text(
                encoding="utf8",
                errors="ignore",
            )
        )
        self.modified = False
        self.editor.setReadOnly(False)
        self.save_action.setEnabled(True)
        self.write("Opened " + path.name)

    def save(self):

        if self.current:

            self.current.write_text(
                self.editor.toPlainText(),
                encoding="utf8",
            )

            self.write("Saved " + self.current.name)

   

    def preview(self):
        self.hugo.preview(self.project)

    def build(self):
        self.hugo.build(self.project)

    def md_help(self):
        show_markdown_help(self)
        
    def update_recent_projects_menu(self):

        self.recent_menu.clear()

        recent = self.settings.recent_projects

        if not recent:

            action = QAction("(Empty)", self)
            action.setEnabled(False)
            self.recent_menu.addAction(action)
            return

        for folder in recent:

            action = QAction(folder, self)

            action.triggered.connect(
                lambda checked=False, p=folder:
                    self.open_recent_project(p)
            )

            self.recent_menu.addAction(action)
            
    def open_recent_project(self, folder):

        folder = Path(folder)

        if not folder.exists():

            QMessageBox.warning(
                self,
                "Missing Project",
                f"{folder}\n\nProject no longer exists."
            )

            return

        self.project = folder

        index = self.model.setRootPath(str(folder))

        self.tree.setModel(self.model)
        self.tree.setRootIndex(index)

        self.settings.last_project = str(folder)
        self.settings.add_recent_project(str(folder))
        self.settings.save()

        self.update_recent_projects_menu()

        self.write(f"Opened {folder}")
        
    def show_context_menu(self, position):

        index = self.tree.indexAt(position)

        if not index.isValid():
            return

        path = Path(self.model.filePath(index))

        menu = QMenu(self)

        new_post = menu.addAction("New Post")
        
        new_folder = menu.addAction("New Folder")

        menu.addSeparator()
        
        rename = menu.addAction("Rename")

        delete = menu.addAction("Delete")


        action = menu.exec(
            self.tree.viewport().mapToGlobal(position)
        )

        if action == new_post:
            self.create_post(path)
            
        elif action == new_folder:
            self.new_folder(path)
        
        elif action == rename:
            self.rename_item(path)

        elif action == delete:
            self.delete_item(path)
                
    def create_post(self, path):

        if path.is_file():
            folder = path.parent
        else:
            folder = path

        title, ok = QInputDialog.getText(
            self,
            "New Post",
            "Post title",
        )

        if not ok or not title:
            return

        slug = title.lower().replace(" ", "-")
    
        file = folder / f"{slug}.md"
        if file.exists():
            QMessageBox.warning(
                self,
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

        self.refresh_tree()

        self.write(f"Created {file}")
        
    def refresh_tree(self):

        if not self.project:
            return

        self.model.setRootPath("")

        index = self.model.setRootPath(
            str(self.project)
        )

        self.tree.setRootIndex(index)
        
    def new_folder(self, path):

        folder = path.parent if path.is_file() else path

        name, ok = QInputDialog.getText(
            self,
            "New Folder",
            "Folder name",
        )

        if not ok or not name:
            return

        new_folder = folder / name

        if new_folder.exists():
            QMessageBox.warning(
                self,
                "Folder exists",
                f"{new_folder.name} already exists."
            )
            return

        new_folder.mkdir()

        self.refresh_tree()

        self.write(f"Created folder {new_folder.name}")
        
    def delete_item(self, path):

        answer = QMessageBox.question(
            self,
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

        self.refresh_tree()

        self.write(f"Deleted {path.name}")
        
    def run_command(self):

        if not self.project:
            return

        command = self.command.text().strip()

        if not command:
            return

        self.write(f"> {command}")

        self.command_process = QProcess(self)

        self.command_process.setWorkingDirectory(str(self.project))

        self.command_process.readyReadStandardOutput.connect(
            lambda: self.write(
                bytes(
                    self.command_process.readAllStandardOutput()
                ).decode(errors="ignore")
            )
        )

        self.command_process.readyReadStandardError.connect(
            lambda: self.write(
                bytes(
                    self.command_process.readAllStandardError()
                ).decode(errors="ignore")
            )
        )

        self.command_process.start("cmd", ["/c", command])

        self.command.clear()
        
    def rename_item(self, path):

        name, ok = QInputDialog.getText(
            self,
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
                self,
                "Already exists",
                f"{name} already exists."
            )
            return

        path.rename(new_path)

        self.refresh_tree()

        self.write(f"Renamed {path.name} → {new_path.name}")
        
    def update_editor_font(self):

        font = self.editor.font()
        font.setPointSize(self.editor_font_size)

        self.editor.setFont(font)
        
    def increase_font_size(self):

        self.editor_font_size += 1
        self.settings.editor_font_size = self.editor_font_size
        self.settings.save()
        self.update_editor_font()
        
    def decrease_font_size(self):

        if self.editor_font_size > 6:
            self.editor_font_size -= 1
            self.settings.editor_font_size = self.editor_font_size
            self.settings.save()
        self.update_editor_font()
        
    def reset_font_size(self):

        self.editor_font_size = 11
        self.settings.editor_font_size = self.editor_font_size
        self.settings.save()
        self.update_editor_font()
        
    def closeEvent(self, event):

        if not self.modified:
            event.accept()
            return
            
    def document_changed(self):

        if self.editor.isReadOnly():
            return

        self.modified = True
    
    def closeEvent(self, event):

        if not self.modified:
            event.accept()
            return

        reply = QMessageBox.question(
            self,
            "Unsaved Changes",
            "Save changes before closing?",
            QMessageBox.Save |
            QMessageBox.Discard |
            QMessageBox.Cancel,
        QMessageBox.Save,
        )
    
        if reply == QMessageBox.Save:
            self.save()
            event.accept()

        elif reply == QMessageBox.Discard:
            event.accept()

        else:
            event.ignore()