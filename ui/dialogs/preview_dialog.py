from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QFormLayout,
    QLineEdit,
)

class PreviewDialog(QDialog):

    def __init__(
        self,
        parent=None,
        settings=None,
        server_running=False,
        server_url="",
    ):
        super().__init__(parent)

        self.settings = settings
        self.server_running = server_running
        self.server_url = server_url

        if self.settings:
            self.preview_settings = self.settings.get_group(
                "preview"
            )
        else:
            self.preview_settings = {}

        self.setWindowTitle("Preview")
        self.resize(600, 450)

        layout = QVBoxLayout(self)
       

        tabs = QTabWidget()
        #------------------------------------------------------
        basic = QWidget()
        basic_layout = QFormLayout(basic)
        self.port_edit = QLineEdit()
        self.port_edit.setText(
            str(self.preview_settings.get("port", 1313))
        )
        basic_layout.addRow("Port:", self.port_edit)

        self.build_drafts_check = QCheckBox("Build Drafts")
        self.build_drafts_check.setChecked(
            self.preview_settings.get("build_drafts", True)
        )
        basic_layout.addRow("", self.build_drafts_check)

        self.disable_fast_render_check = QCheckBox(
            "Disable Fast Render"
        )
        self.disable_fast_render_check.setChecked(
            self.preview_settings.get(
                "disable_fast_render",
                True,
            )
        )
        basic_layout.addRow("", self.disable_fast_render_check)

        self.open_browser_check = QCheckBox(
            "Open Browser"
        )
        self.open_browser_check.setChecked(
            self.preview_settings.get(
                "open_browser",
                True,
            )
        )
        basic_layout.addRow("", self.open_browser_check)
        
        #--------------------------------------
        
        advanced = QWidget()
        advanced_layout = QFormLayout(advanced)
        self.build_future_check = QCheckBox("Build Future")
        self.build_future_check.setChecked(
            self.preview_settings.get(
                "build_future",
                False,
            )
        )
        advanced_layout.addRow("", self.build_future_check)

        self.build_expired_check = QCheckBox("Build Expired")
        self.build_expired_check.setChecked(
            self.preview_settings.get(
                "build_expired",
                False,
            )
        )
        advanced_layout.addRow("", self.build_expired_check)

        self.base_url_edit = QLineEdit()
        self.base_url_edit.setText(
            self.preview_settings.get(
                "base_url",
                "",
            )
        )
        advanced_layout.addRow(
            "Base URL:",
            self.base_url_edit,
        )

        self.navigate_changed_check = QCheckBox(
            "Navigate to Changed"
        )
        self.navigate_changed_check.setChecked(
            self.preview_settings.get(
                "navigate_to_changed",
                False,
            )
        )
        advanced_layout.addRow(
            "",
            self.navigate_changed_check,
        )

        self.verbose_check = QCheckBox(
            "Verbose Logging"
        )
        self.verbose_check.setChecked(
            self.preview_settings.get(
                "verbose",
                False,
            )
        )
        advanced_layout.addRow("", self.verbose_check)

        self.path_warnings_check = QCheckBox(
            "Print Path Warnings"
        )
        self.path_warnings_check.setChecked(
            self.preview_settings.get(
                "print_path_warnings",
                False,
            )
        )
        advanced_layout.addRow("", self.path_warnings_check)
        
        #-----------------------------------------------------
        
        tabs.addTab(basic, "Basic")
        tabs.addTab(advanced, "Advanced")

        layout.addWidget(tabs)
        
        
        layout.addWidget(QLabel("Command Preview"))
        self.command_preview = QPlainTextEdit()
        self.command_preview.setReadOnly(True)
        self.command_preview.setMaximumHeight(70)
        layout.addWidget(self.command_preview)
        

        self.remember_check = QCheckBox(
            "Remember these settings"
        )
        
        self.stop_button = QPushButton("Stop Preview")

        remember_layout = QHBoxLayout()
        remember_layout.addWidget(self.remember_check)
        remember_layout.addStretch()
        remember_layout.addWidget(self.stop_button)

        layout.addLayout(remember_layout)
        
        
     

        
        
         ##################################x
        
        self.status_label = QLabel()

        if self.server_running:
            self.status_label.setText(
                f"🟢 Preview is running at {self.server_url}.\n\n"
                "Stop the preview server to modify these settings."
            )
        else:
            self.status_label.setText(
                "⚪ Preview is not running."
            )

        layout.addWidget(self.status_label)
        #######################################

        buttons = QHBoxLayout()
        buttons.addStretch()

        self.run_button = QPushButton("Run")
        self.close_button = QPushButton("Close")

        buttons.addWidget(self.run_button)
        buttons.addWidget(self.close_button)

        layout.addLayout(buttons)
        
        
        ##############################
        self.option_widgets = [
            self.port_edit,
            self.build_drafts_check,
            self.disable_fast_render_check,
            self.open_browser_check,
            self.build_future_check,
            self.build_expired_check,
            self.base_url_edit,
            self.navigate_changed_check,
            self.verbose_check,
            self.path_warnings_check,
        ]
        ######################################   
        self.run_button.clicked.connect(self.accept)
        self.close_button.clicked.connect(self.reject)
        self.stop_button.setEnabled(
            self.server_running
        )
        
        
        self.stop_button.clicked.connect(
            self.stop_preview
        )
        
        
        #------------------------------------------
        
        self.port_edit.textChanged.connect(
            self.update_command_preview
        )

        self.build_drafts_check.toggled.connect(
            self.update_command_preview
        )

        self.disable_fast_render_check.toggled.connect(
            self.update_command_preview
        )

        self.open_browser_check.toggled.connect(
            self.update_command_preview
        )

        self.build_future_check.toggled.connect(
            self.update_command_preview
        )

        self.build_expired_check.toggled.connect(
            self.update_command_preview
        )

        self.base_url_edit.textChanged.connect(
            self.update_command_preview
        )

        self.navigate_changed_check.toggled.connect(
            self.update_command_preview
        )

        self.verbose_check.toggled.connect(
            self.update_command_preview
        )

        self.path_warnings_check.toggled.connect(
            self.update_command_preview
        )

        self.update_command_preview()
        
        self.set_options_enabled(
        not self.server_running
        )
        
        
        #-------------------------------------------
        
    def update_command_preview(self):

        options = self.options()

        command = (
            self.parent()
                .hugo
                .preview_command(options)
        )

        self.command_preview.setPlainText(
            " ".join(command)
        )
        
    def options(self):

        port = self.port_edit.text().strip() or "1313"

        try:
            port_number = int(port)

            if not (1 <= port_number <= 65535):
                port_number = 1313

        except ValueError:
            port_number = 1313

        return {
            "port": str(port_number),
            "build_drafts": self.build_drafts_check.isChecked(),
            "disable_fast_render": (
                self.disable_fast_render_check.isChecked()
            ),
            "open_browser": self.open_browser_check.isChecked(),
            "build_future": self.build_future_check.isChecked(),
            "build_expired": self.build_expired_check.isChecked(),
            "base_url": self.base_url_edit.text().strip(),
            "navigate_to_changed": (
                self.navigate_changed_check.isChecked()
            ),
            "verbose": self.verbose_check.isChecked(),
            "print_path_warnings": (
                self.path_warnings_check.isChecked()
            ),
        }
        
        
    def accept(self):

        if self.settings and self.remember_check.isChecked():
            self.settings.set_group(
                "preview",
                self.options()
            )
            self.settings.save()

        super().accept()
        
    def set_options_enabled(self, enabled):

        for widget in self.option_widgets:
            widget.setEnabled(enabled)

        self.remember_check.setEnabled(enabled)
        self.run_button.setEnabled(enabled)
        
        
    def stop_preview(self):

        self.parent().hugo.stop_server()

        self.server_running = False

        self.set_options_enabled(True)

        self.stop_button.setEnabled(False)

        self.status_label.setText(
            "⚪ Preview is not running.\n\n"
            "You can now modify the preview settings."
        )
        