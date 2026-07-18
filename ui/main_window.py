import datetime
from pathlib import Path
import shutil
from textwrap import dedent


from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QProcess

from PySide6.QtWidgets import (
    QFileDialog,
    QFileSystemModel,
    QHBoxLayout,
    QInputDialog,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSplitter,
    QTabWidget,
    QTextBrowser,
    QTreeView,
    QVBoxLayout,
    QWidget,
)


from core.hugo_service import HugoService
from core.settings import Settings
from core.themes import THEMES
from authoring.markdown_actions import MarkdownActions
from ui.authoring_toolbar import AuthoringToolbar
from ui.document_editor import DocumentEditor

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
       
        self.settings = Settings()
        self.editor_font_size = self.settings.editor_font_size
        self.project = None
       

        self.hugo = HugoService(self)

        self.resize(1200, 700)
        self.setWindowTitle("Hugo Studio v0.4.2 Alpha")

        self.build_ui()

        self.restore_last_project()
        
    def build_menus(self):

        menu = self.menuBar()

        self.build_file_menu(menu)
        self.build_view_menu(menu)
        self.build_hugo_menu(menu)
        self.build_theme_menu(menu)
        self.build_help_menu(menu)
        


    def build_file_menu(self, menu):

        file_menu = menu.addMenu("&File")
        new_project = QAction("New Project...", self)
        new_project.triggered.connect(self.new_project)
        file_menu.addAction(new_project)

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

    def build_view_menu(self, menu):

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
        
    def build_hugo_menu(self, menu):

        hugo_menu = menu.addMenu("&Hugo")

        preview_action = QAction("Preview", self)
        preview_action.setShortcut("F5")
        preview_action.triggered.connect(self.preview)
        hugo_menu.addAction(preview_action)

        build_action = QAction("Build", self)
        build_action.setShortcut("F6")
        build_action.triggered.connect(self.build)
        hugo_menu.addAction(build_action)

        hugo_menu.addSeparator()
        
    def build_theme_menu(self, menu):

        theme_menu = menu.addMenu("&Theme")

        install_theme_action = QAction("Install Theme...", self)
        install_theme_action.triggered.connect(self.install_theme)
        theme_menu.addAction(install_theme_action)
 
    def build_help_menu(self, menu):

        help_menu = menu.addMenu("&Help")

        help_action = QAction("Markdown Help", self)
        help_action.setShortcut("F1")
        help_action.triggered.connect(self.md_help)
        help_menu.addAction(help_action)

    def build_ui(self):

 
        self.build_menus()

        splitter = QSplitter()
        self.setCentralWidget(splitter)

        self.model = QFileSystemModel()
        self.model.setReadOnly(False)

        self.tree = QTreeView()
        self.tree.setDragEnabled(True)
        self.tree.setAcceptDrops(True)
        self.tree.setDropIndicatorShown(True)
        self.tree.setDragDropMode(QTreeView.InternalMove)
        
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        self.tree.clicked.connect(self.open_file)

        splitter.addWidget(self.tree)

        right = QWidget()
        layout = QVBoxLayout(right)
      

        self.welcome = QTextBrowser()
        self.welcome.setHtml("""
        <h2>Welcome to Hugo Studio</h2>
        <p>Open a Markdown file or create a new post.</p>
        """)
        
        
        
        self.md = MarkdownActions(self.current_editor)
        self.authoring = AuthoringToolbar(self.md)
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        
        
        self.tabs.addTab(
            self.welcome,
            "Welcome",
        )

        layout.addWidget(self.authoring)
  
        layout.addWidget(self.tabs)

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
        
        self.statusBar().showMessage("No project open")
        

       
        
    # --------------------

    def write(self, message):
        self.log.appendPlainText(message)

    def restore_last_project(self):

        folder = self.settings.last_project

        if not folder:
            return

        self.reset_editor()

        self.load_project(folder)
        
    def open_project(self):

        if not self.maybe_save():
            return

        self.reset_editor()

        folder = QFileDialog.getExistingDirectory(
            self,
            "Project",
        )

        if not folder:
            return

        self.load_project(folder)
        
        
    def open_file(self, index):

        path = Path(self.model.filePath(index))

        if path.is_dir():
            return

        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)

            if (
                isinstance(widget, DocumentEditor)
                and widget.file_path == path
            ):
                self.tabs.setCurrentIndex(i)
                return

        self.load_file(path)

    def save(self):

        editor = self.current_editor()

        if editor is None:
            return

        if editor.file_path is None:
            return

        editor.file_path.write_text(
            editor.toPlainText(),
            encoding="utf8",
        )

        editor.modified = False

        self.tabs.setTabText(
            self.tabs.currentIndex(),
            editor.file_path.name,
        )

        self.write(f"Saved {editor.file_path.name}")

        self.update_status()

   

    def preview(self):
        
        
        self.hugo.preview(self.project)

    def build(self):
        self.hugo.build(self.project)

    def md_help(self):

        # Is it already open?
        for i in range(self.tabs.count()):

            if self.tabs.tabText(i) == "Markdown Help":
                self.tabs.setCurrentIndex(i)
                return

        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setReadOnly(True)
        
        
         

        help_file = Path("docs/markdown_help.md")

        if help_file.exists():

            browser.setMarkdown(
                    help_file.read_text(
                        encoding="utf8"
                    )
            )

        else:

            browser.setMarkdown(
                "# Help\n\n"
                "Help file not found."
            )

        index = self.tabs.addTab(
            browser,
            "Markdown Help",
        )
        


        self.tabs.setCurrentIndex(index)
        
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

        if not self.maybe_save():
            return

        self.reset_editor()

        self.load_project(folder)
        
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
            
        # Is the currently active file gone?
        editor = self.current_editor()

        if (
            editor is not None
            and editor.file_path is not None
            and editor.file_path == path
        ):
            self.close_tab(self.tabs.currentIndex())


        self.refresh_tree()

        self.write(f"Deleted {path.name}")
        
    def run_command(self):

        if not self.project:
            return

        command = self.command.text().strip()

        if not command:
            return

        self.hugo.run_command(command)

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
        
    def update_editor_font(self, editor):

        font = editor.font()
        font.setPointSize(self.editor_font_size)
        editor.setFont(font)


    def increase_font_size(self):

        self.editor_font_size += 1
        self.settings.editor_font_size = self.editor_font_size
        self.settings.save()

        for i in range(self.tabs.count()):

            widget = self.tabs.widget(i)

            if isinstance(widget, DocumentEditor):
                self.update_editor_font(widget)


    def decrease_font_size(self):

        if self.editor_font_size > 6:
            self.editor_font_size -= 1
            self.settings.editor_font_size = self.editor_font_size
            self.settings.save()

        for i in range(self.tabs.count()):

            widget = self.tabs.widget(i)

            if isinstance(widget, DocumentEditor):
                self.update_editor_font(widget)


    def reset_font_size(self):

        self.editor_font_size = 11
        self.settings.editor_font_size = self.editor_font_size
        self.settings.save()

        for i in range(self.tabs.count()):

            widget = self.tabs.widget(i)

            if isinstance(widget, DocumentEditor):
                self.update_editor_font(widget)


 


    def create_editor(self):

        editor = DocumentEditor()

        self.update_editor_font(editor)
        editor.textChanged.connect(self.document_changed)

        return editor
            
    def closeEvent(self, event):
            
        self.hugo.stop_server()
        if self.maybe_save():
            event.accept()
        else:
            event.ignore()
            
    def document_changed(self):

        editor = self.current_editor()

        if editor is None:
            return

        if editor.isReadOnly():
            return

        if editor.modified:
            return

        editor.modified = True

        if editor.file_path:

            self.tabs.setTabText(
                self.tabs.currentIndex(),
                editor.file_path.name + " *",
            )

        self.update_status()
    
    
            
            
    def new_project(self):

        if not self.maybe_save():
            return

        name, ok = QInputDialog.getText(
            self,
            "New Project",
            "Project name:",
        )

        if not ok or not name.strip():
            return

        name = name.strip()

        workspace = QFileDialog.getExistingDirectory(
            self,
            "Select Workspace",
        )

        if not workspace:
            return

        project = Path(workspace) / name

        if project.exists():

            QMessageBox.warning(
                self,
                "Project Exists",
                f"{project}\n\nChoose another project name.",
            )
            return

        self.reset_editor()

        if self.hugo.new_project(workspace, name):
           self.load_project(project)
        else:
            
            QMessageBox.critical(
            self,
                "Project Creation Failed",
        "Hugo Studio could not create the project.\n\nCheck the log for details.",
            )
     
        
        
    def install_theme(self):

       

        theme, ok = QInputDialog.getItem(
            self,
            "Install Theme",
            "Choose a theme:",
            sorted(THEMES.keys()),
            0,
            False,
        )

        if not ok:
            return

        self.hugo.install_theme(
            self.project,
            theme,
        )
    def update_status(self):

        if self.project is None:
            self.statusBar().showMessage("No project open")
            return

        project = self.project.name

        editor = self.current_editor()

        if editor is None or editor.file_path is None:
            self.statusBar().showMessage(
                f"Project: {project}"
            )
        else:
            self.statusBar().showMessage(
                f"Project: {project} | File: {editor.file_path.name}"
            )
            
    def maybe_save(self):

        editor = self.current_editor()

        if editor is None:
            return True

        if not editor.modified:
            return True

        reply = QMessageBox.question(
            self,
            "Unsaved Changes",
            f"Save changes to {editor.file_path.name}?",
            QMessageBox.Save |
            QMessageBox.Discard |
            QMessageBox.Cancel,
            QMessageBox.Save,
        )

        if reply == QMessageBox.Save:
            self.save()
            return True

        if reply == QMessageBox.Discard:
            return True

        return False
        
    def reset_editor(self):

        while self.tabs.count() > 1:

            widget = self.tabs.widget(1)

            self.tabs.removeTab(1)

            widget.deleteLater()

        self.save_action.setEnabled(False)

        self.tabs.setCurrentIndex(0)

        self.update_status()
        
    def load_file(self, path):

        editor = self.create_editor()

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

        self.save_action.setEnabled(True)

        index = self.tabs.addTab(
            editor,
            path.name,
        )

        self.tabs.setCurrentIndex(index)
        editor.setFocus()

        self.write("Opened " + path.name)

        self.update_status()
        
    
        
    def load_project(self, folder):

        folder = Path(folder)

        if not folder.exists():

            QMessageBox.warning(
                self,
                "Missing Project",
                f"{folder}\n\nProject no longer exists."
            )

            return False

        self.project = folder
    
        index = self.model.setRootPath(str(folder))

        self.tree.setModel(self.model)
        self.tree.setRootIndex(index)

        self.settings.last_project = str(folder)
        self.settings.add_recent_project(str(folder))
        self.settings.save()

        self.update_recent_projects_menu()

        self.write(f"Opened {folder}")

        self.update_status()

        return True
        
        
    def close_tab(self, index):

        widget = self.tabs.widget(index)

        if widget == self.welcome:
            self.tabs.removeTab(index)
            widget.deleteLater()
            return

        self.tabs.setCurrentIndex(index)

        if not self.maybe_save():
            return

        self.tabs.removeTab(index)

        widget.deleteLater()
        if self.current_editor() is None:
            self.save_action.setEnabled(False)

        self.update_status()
        

        
    def current_editor(self):

        widget = self.tabs.currentWidget()

        if isinstance(widget, DocumentEditor):
            return widget

        return None


    def current_file(self):

        editor = self.current_editor()

        if editor:
            return editor.file_path

        return None