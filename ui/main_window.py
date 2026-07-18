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
    QApplication,
)

from core.version import RELEASE
from core.hugo_service import HugoService
from core.settings import Settings
from core.themes import THEMES
from authoring.markdown_actions import MarkdownActions
from ui.authoring_toolbar import AuthoringToolbar
from ui.document_editor import DocumentEditor
from ui.mainwindow.menus import build_menus
from ui.mainwindow.tree import show_context_menu

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
       
        self.settings = Settings()
        self.editor_font_size = self.settings.editor_font_size
        self.project = None
       

        self.hugo = HugoService(self)

        self.resize(1200, 700)
        self.setWindowTitle(
            f"{QApplication.applicationName()} "
            f"v{QApplication.applicationVersion()} {RELEASE}"
        )

        self.build_ui()

        self.restore_last_project()
        
    

    def build_ui(self):
 
        build_menus(self)

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
        self.tree.clicked.connect(self.open_file)
        
     

        self.tree.customContextMenuRequested.connect(
            lambda pos: show_context_menu(self, pos)
        )

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
        
   
        
    def run_command(self):

        if not self.project:
            return

        command = self.command.text().strip()

        if not command:
            return

        self.hugo.run_command(command)

        self.command.clear()
        
    
        
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