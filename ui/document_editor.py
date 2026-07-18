from pathlib import Path
from PySide6.QtWidgets import QPlainTextEdit


class DocumentEditor(QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.file_path: Path | None = None
        self.modified = False