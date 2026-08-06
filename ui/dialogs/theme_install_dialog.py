from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QTabWidget,
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QLineEdit,
    QCheckBox,
    QPlainTextEdit,
)

from PySide6.QtGui import QFont
from PySide6.QtCore import Qt
from pathlib import Path



class ThemeInstallDialog(QDialog):
    def __init__(self, parent=None, settings=None):
        super().__init__(parent)
        self.settings = settings

        if self.settings:
            self.theme_settings = self.settings.get_group("theme")
        else:
            self.theme_settings = {}
        
        

        self.setWindowTitle("Install Theme")
        self.resize(600, 450)

        layout = QVBoxLayout(self)

        tabs = QTabWidget()

        # Basic tab
        basic = QWidget()
        basic_layout = QVBoxLayout(basic)

        basic_layout.addWidget(QLabel(
            "<h3>Install a Hugo Theme (ZIP)</h3>"
        ))

        text = QLabel(
            """
            <p>
            Browse themes on the
            <a href="https://themes.gohugo.io/">official Hugo Themes website</a>.
            Each theme links to its GitHub repository, where you can download the ZIP archive
            (<b>Code → Download ZIP</b>).
            </p>

            <p><b>TOML</b></p>

            <pre>theme = "PaperMod"</pre>

            <p>If your project uses <b>YAML</b>, use:</p>

            <pre>theme: PaperMod</pre>

            <p>
            Most Hugo theme documentation uses TOML examples. If your project uses
            <b>hugo.yaml</b>, simply convert the examples to YAML syntax.
            </p>
            """
        )

        text.setOpenExternalLinks(True)
        text.setWordWrap(True)
        
        

        basic_layout.addWidget(text)
        

        basic_layout.addStretch()

        tabs.addTab(basic, "Basic")
        
        # Advanced tab
        advanced = self.create_advanced_tab()
        tabs.addTab(advanced, "Advanced")
        

        layout.addWidget(tabs)
        
        
        # self.remember_check = QCheckBox("Remember these settings")
        # layout.addWidget(self.remember_check)
        
        buttons = QHBoxLayout()
        buttons.addStretch()
        
    

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        
        

        buttons.addWidget(self.close_button)

        layout.addLayout(buttons)
        
        
        
    def create_advanced_tab(self):

        tab = QWidget()
        layout = QVBoxLayout(tab)

        # Title
        layout.addWidget(QLabel("<h3>Install a Hugo Theme with Git</h3>"))

        # Instructions
        text = QLabel(
            '<p>'
            'Browse themes on the '
            '<a href="https://themes.gohugo.io/">official Hugo Themes website</a>.<br><br>'
            'Open the theme\'s page, follow the <b>Repository</b> link to GitHub.<br>'
            'Click <b>Code</b> and copy the <b>HTTPS</b> repository URL.'
            '</p>'
        )

        text.setOpenExternalLinks(True)
        text.setWordWrap(True)

        layout.addWidget(text)

        # Repository URL
        layout.addWidget(QLabel("<b>Repository URL</b>"))

        self.repo_edit = QLineEdit()
        self.repo_edit.setPlaceholderText(
            "https://github.com/owner/theme.git"
        )

        layout.addWidget(self.repo_edit)

        # Git Clone preview
        layout.addWidget(QLabel("<b>Command preview</b>"))
        
        self.clone_preview = QPlainTextEdit()
        font = QFont("Consolas")
        font.setStyleHint(QFont.Monospace)
        self.clone_preview.setFont(font)
        self.clone_preview.setReadOnly(True)
        self.clone_preview.setMaximumHeight(60)

        layout.addWidget(self.clone_preview)
        self.clone_button = QPushButton("Run")
        layout.addWidget(self.clone_button)
        self.clone_button.clicked.connect(self.execute_git_clone)
        self.repo_edit.textChanged.connect(self.update_clone_preview)

        layout.addStretch()

        return tab
        
    def update_clone_preview(self):

        url = self.repo_edit.text().strip()

        if not url:
            self.clone_preview.clear()
            return

        theme_name = self.theme_name_from_repo(url)

        command = f"git clone {url} themes/{theme_name}"

        self.clone_preview.setPlainText(command)
        
    def execute_git_clone(self):

        window = self.parent()
        
       

        repo_url = self.repo_edit.text().strip()

        if not repo_url:
            return

        theme_name = self.theme_name_from_repo(repo_url)
        self.set_installing(True)
        
        
        window.hugo.install_theme(
            window.project,
            repo_url,
            theme_name,
            self,
        )
        
    def theme_name_from_repo(self, repo_url):
        name = Path(repo_url).stem

        prefixes = (
            "hugo-theme-",
            "hugo-",
            "theme-",
        )

        for prefix in prefixes:
            if name.lower().startswith(prefix):
                name = name[len(prefix):]
                break

        return name
        
    def set_installing(self, installing):

        self.clone_button.setEnabled(not installing)
        self.repo_edit.setEnabled(not installing)
        self.close_button.setEnabled(not installing)

        if installing:
            self.clone_button.setText("Installing...")
        else:
            self.clone_button.setText("Execute Git Clone")
            
            
    def closeEvent(self, event):

        

        if not self.clone_button.isEnabled():
            event.ignore()
            return

        super().closeEvent(event)