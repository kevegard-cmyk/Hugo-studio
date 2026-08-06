from pathlib import Path

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QPlainTextEdit,
    QLabel,
)

from core.project_options import NewProjectOptions


class NewProjectDialog(QDialog):
    def __init__(
        self,
        parent=None,
        settings=None,
        default_workspace="",
        config_format="toml",
        initialize_git=False,
    ):
        
        
        super().__init__(parent)
        
        self.settings = settings
        
        if self.settings:
            self.new_project_settings = self.settings.get_group(
                "new_project"
            )
        else:
            self.new_project_settings = {}

        self.setWindowTitle("New Hugo Project")
        self.setMinimumWidth(460)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("my-hugo-site")

        self.location_edit = QLineEdit(default_workspace)
        
        default_workspace = self.new_project_settings.get(
            "default_workspace",
            default_workspace,
        )

        self.location_edit.setText(default_workspace)
        
        self.location_edit.setPlaceholderText("Choose a workspace folder")

        self.format_combo = QComboBox()
        self.format_combo.addItem("TOML (.toml)", "toml")
        self.format_combo.addItem("YAML (.yaml)", "yaml")
        json_index = self.format_combo.count()
        self.format_combo.addItem("JSON (.json) — unavailable", "json")
        self.format_combo.model().item(json_index).setEnabled(False)
        self.format_combo.model().item(json_index).setToolTip(
            "Disabled because the installed Hugo version creates an invalid "
            "JSON archetype."
        )

        if config_format not in {"toml", "yaml"}:
            config_format = "toml"
            
        config_format = self.new_project_settings.get(
            "config_format",
            config_format,
        )

        self.format_combo.setCurrentIndex(
            max(0, self.format_combo.findData(config_format))
        )

        self.git_check = QCheckBox("Initialize a Git repository")

        initialize_git = self.new_project_settings.get(
            "initialize_git",
            initialize_git,
        )

        self.git_check.setChecked(initialize_git)

        tabs = QTabWidget()
        tabs.addTab(self.create_details_tab(), "Details")
        tabs.addTab(self.create_advanced_tab(), "Advanced")
        self.remember_check = QCheckBox("Remember these settings")
        
        self.command_preview = QPlainTextEdit()
        self.command_preview.setReadOnly(True)
        self.command_preview.setMaximumHeight(60)

        

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(
            QDialogButtonBox.StandardButton.Ok
        ).setText("Create Project")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

       
        
        layout = QVBoxLayout(self)
        layout.addWidget(tabs)
        layout.addWidget(QLabel("Command Preview"))
        layout.addWidget(self.command_preview)
        layout.addWidget(self.remember_check)
        layout.addWidget(buttons)
        
        self.name_edit.textChanged.connect(
            self.update_command_preview
        )

        self.location_edit.textChanged.connect(
            self.update_command_preview
        )

        self.format_combo.currentIndexChanged.connect(
            self.update_command_preview
        )

        self.git_check.toggled.connect(
            self.update_command_preview
        )
        
        self.update_command_preview()

    def create_details_tab(self):
        tab = QWidget()
        layout = QFormLayout(tab)

        browse_button = QPushButton("Browse…")
        browse_button.clicked.connect(self.choose_location)

        location_layout = QHBoxLayout()
        location_layout.setContentsMargins(0, 0, 0, 0)
        location_layout.addWidget(self.location_edit)
        location_layout.addWidget(browse_button)

        layout.addRow("Project name:", self.name_edit)
        layout.addRow("Location:", location_layout)

        return tab

    def create_advanced_tab(self):
        tab = QWidget()
        layout = QFormLayout(tab)

        layout.addRow("Configuration format:", self.format_combo)
        layout.addRow("", self.git_check)

        return tab

    def choose_location(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Workspace",
            self.location_edit.text(),
        )

        if folder:
            self.location_edit.setText(folder)

    def accept(self):
        name = self.name_edit.text().strip()
        folder = Path(self.location_edit.text().strip())

        if (
            not name
            or Path(name).is_absolute()
            or len(Path(name).parts) != 1
            or name in {".", ".."}
        ):
            QMessageBox.warning(
                self,
                "Invalid Project Name",
                "Enter a single folder name without paths.",
            )
            return

        if not folder.is_dir():
            QMessageBox.warning(
                self,
                "Invalid Location",
                "Choose an existing workspace folder.",
            )
            return
            
        if self.settings and self.remember_check.isChecked():
            
            self.new_project_settings["default_workspace"] = (
                self.location_edit.text().strip()
            )

            self.new_project_settings["initialize_git"] = (
                self.git_check.isChecked()
            )

            self.new_project_settings["config_format"] = (
                self.format_combo.currentData()
            )

            self.settings.save()

        super().accept()
        
        
        
    def update_command_preview(self):

        name = self.name_edit.text().strip()
        folder = self.location_edit.text().strip()
        config = self.format_combo.currentData()

        if not name or not folder:
            self.command_preview.clear()
            return

        project_path = Path(folder) / name

        command = (
            f'hugo new site "{project_path}" '
            f'--format {config}'
        )

        if self.git_check.isChecked():
            command += "\n\ngit init"

        self.command_preview.setPlainText(command)

    def options(self):
        return NewProjectOptions(
            parent_folder=Path(self.location_edit.text().strip()),
            name=self.name_edit.text().strip(),
            config_format=self.format_combo.currentData(),
            initialize_git=self.git_check.isChecked(),
        )
