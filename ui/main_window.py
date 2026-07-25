import datetime
from pathlib import Path
import shutil
from textwrap import dedent

from PySide6.QtGui import QAction
from PySide6.QtCore import Qt, QProcess
from ui.image_viewer import ImageViewer

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
    QLabel,
    QStackedWidget,
    QAbstractItemView,
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
from ui.mainwindow.project import (
    restore_last_project,
    update_recent_projects_menu,
)
from core.installation_check import check_installation
from ui.dialogs.installation_dialog import InstallationDialog
from ui.dialogs.about_dialog import AboutDialog

from ui.mainwindow.editor import (
    create_editor_actions,
    load_file,
    save,
    save_as,
    close_tab,
    current_editor,
    is_editable_file,
)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.settings = Settings()

        if self.settings.first_run:

            result = check_installation()

            self.settings.hugo_available = result["hugo"]
            self.settings.git_available = result["git"]
            self.settings.first_run = False
            self.settings.save()

            InstallationDialog(result, self).exec()

        self.editor_font_size = self.settings.editor_font_size
        self.project = None

        self.hugo = HugoService(self)

        self.resize(1200, 700)
        self.setWindowTitle(
            f"{QApplication.applicationName()} "
            f"v{QApplication.applicationVersion()} {RELEASE}"
        )

        self.build_ui()

        restore_last_project(self)
        
    
    def build_ui(self):
        
        
 
        self.save_action, self.save_as_action = create_editor_actions(self)
        build_menus(self)
        
        

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        splitter = QSplitter()

        self.model = QFileSystemModel()
        self.model.setReadOnly(False)
           
        self.tree = QTreeView()
        self.tree.setHeaderHidden(True)
        self.tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
        empty_page = QWidget()
        empty_layout = QVBoxLayout(empty_page)

        self.empty_project_label = QLabel(
            "Project Explorer\n\nNo project open."
        )
        self.empty_project_label.setAlignment(Qt.AlignHCenter)

        empty_layout.addWidget(self.empty_project_label)
        empty_layout.setContentsMargins(10, 20, 10, 10)
        empty_layout.addStretch()

        self.project_stack = QStackedWidget()
        self.project_stack.addWidget(empty_page)   # index 0
        self.project_stack.addWidget(self.tree)    # index 1
        # self.tree.setDragEnabled(True)
        # self.tree.setAcceptDrops(True)
        # self.tree.setDropIndicatorShown(True)
        # self.tree.setDragDropMode(QTreeView.InternalMove)
        
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        #self.tree.clicked.connect(self.open_file)
        self.tree.doubleClicked.connect(self.open_file)
     

        self.tree.customContextMenuRequested.connect(
            lambda pos: show_context_menu(self, pos)
        )

        splitter.addWidget(self.project_stack)

        right = QWidget()
        layout = QVBoxLayout(right)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
      

        self.welcome = QTextBrowser()
        self.welcome.setHtml("""
        <h2>Welcome to Hugo Studio</h2>
        <p>A desktop IDE for Hugo websites.</p>
        <hr>
        <p><b>Start by:</b></p>
        <ul>
            <li>Creating a new project</li>
            <li>Opening an existing project</li>
            <li>Editing Markdown content</li>
            <li>Previewing your site locally</li>
            <li>Building your website for deployment</li>
        </ul>
        <p>Your project files will appear in the Project Explorer once a project is open.</p>
        """)
     
        
        self.md = MarkdownActions(
            lambda: current_editor(self)
        )
        
       

        self.authoring = AuthoringToolbar(
            self.md,
            self.save_action,
            self.save_as_action,
        )
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(
            lambda index: close_tab(self, index)
        )
           
        
        self.tabs.addTab(
            self.welcome,
            "Welcome",
        )

        
  
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

        main_layout.addWidget(self.authoring, 0)
        main_layout.addWidget(splitter, 1)
        
        update_recent_projects_menu(self)
        
        self.update_status()
        
        self.update_project_view()

    def write(self, message):
        self.log.appendPlainText(message)
 
    def open_file(self, index):

        path = Path(self.model.filePath(index))

        if path.is_dir():
            return

        if path.suffix.lower() in {
            ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"
        }:
            ImageViewer(path, self).exec()
            return

        if not is_editable_file(path):
            self.statusBar().showMessage(
                f"'{path.name}' is not an editable text file.",
                3000
            )
            return

        for i in range(self.tabs.count()):
            widget = self.tabs.widget(i)

            if (
                isinstance(widget, DocumentEditor)
                and widget.file_path == path
            ):
                self.tabs.setCurrentIndex(i)
                return

        load_file(self, path)

    def preview(self):
        self.hugo.preview(self.project)

    def build(self):
        self.hugo.build(self.project)

    def md_help(self):

        # Is it already open?
        for i in range(self.tabs.count()):

            if self.tabs.tabText(i) == "HugoStudio Help":
                self.tabs.setCurrentIndex(i)
                return

        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setReadOnly(True)
  
        help_file = Path("docs/hugostudio_help.md")
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
            "HugoStudio Help",
        )
        
        self.tabs.setCurrentIndex(index)
           
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
            
    # def closeEvent(self, event):
            
        # self.hugo.stop_server()
        # if self.maybe_save():
            # event.accept()
        # else:
            # event.ignore()
            
    # def closeEvent(self, event):
        # if not self.maybe_save_all():
            # event.ignore()
            # return

        # self.hugo.stop_server()
        # event.accept()
        
    def closeEvent(self, event):
        if not self.maybe_save_all():
            event.ignore()
            return

        self.hugo.stop_server()
        event.accept()
                  
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
        

            
    def maybe_save(self):

        editor = current_editor(self)

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
            save(self)
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
        self.save_as_action.setEnabled(False)

        self.tabs.setCurrentIndex(0)

        self.update_status()
        
        
    def update_status(self):
        self.statusBar().clearMessage()



            
    def update_window_title(self):
        title = (
            f"{QApplication.applicationName()} "
            f"v{QApplication.applicationVersion()} {RELEASE}"
        )

        if self.project:
            title += f" — {self.project.name}"
        else:
            title += " — No project open"

        self.setWindowTitle(title)
            
    def update_project_view(self):
        if self.project is None:
            self.project_stack.setCurrentIndex(0)
        else:
            self.project_stack.setCurrentIndex(1)
            
            
    def maybe_save_all(self):
        original_index = self.tabs.currentIndex()

        for index in range(self.tabs.count()):
            widget = self.tabs.widget(index)

            if not isinstance(widget, DocumentEditor):
                continue

            if not widget.modified:
                continue

            self.tabs.setCurrentIndex(index)

            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                f"Save changes to {widget.file_path.name}?",
                QMessageBox.Save
                | QMessageBox.Discard
                | QMessageBox.Cancel,
                QMessageBox.Save,
            )

            if reply == QMessageBox.Save:
                save(self)

            elif reply == QMessageBox.Cancel:
                self.tabs.setCurrentIndex(original_index)
                return False

        self.tabs.setCurrentIndex(original_index)
        return True
        
    def create_editor_actions(self):
        self.save_action = QAction("Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.setShortcutContext(Qt.WindowShortcut)
        self.save_action.setEnabled(False)
        self.save_action.triggered.connect(lambda: save(self))

        self.addAction(self.save_action)

        self.save_as_action = QAction("Save As…", self)
        self.save_as_action.setEnabled(False)
        self.save_as_action.triggered.connect(lambda: save_as(self))
        
    def show_about(self):
        AboutDialog(self).exec()