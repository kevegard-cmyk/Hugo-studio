from pathlib import Path
import datetime

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QToolBar,
    QFileDialog,
    QFileSystemModel,
    QTreeView,
    QSplitter,
    QPlainTextEdit,
    QPushButton,
    QInputDialog,
)

from utils.markdown_highlighter import MarkdownHighlighter
from ui.markdown_help import show_markdown_help
from core.hugo_service import HugoService


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.project = None
        self.current = None

        self.hugo = HugoService(self)

        self.resize(1200, 700)
        self.setWindowTitle("Hugo Studio v0.3")

        self.build_ui()

    def build_ui(self):

        toolbar = self.addToolBar("Main")

        for name, fn in [
            ("Open", self.open_project),
            ("New", self.new_post),
            ("Save", self.save),
            ("Preview", self.preview),
            ("Build", self.build),
            ("MD Help", self.md_help),
        ]:
            action = toolbar.addAction(name)
            action.triggered.connect(fn)

        splitter = QSplitter()
        self.setCentralWidget(splitter)

        self.model = QFileSystemModel()

        self.tree = QTreeView()
        self.tree.clicked.connect(self.open_file)

        splitter.addWidget(self.tree)

        right = QWidget()
        layout = QVBoxLayout(right)

        self.editor = QPlainTextEdit()
        MarkdownHighlighter(self.editor.document())

        layout.addWidget(self.editor)

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setMaximumHeight(140)

        layout.addWidget(self.log)

        splitter.addWidget(right)

        splitter.setSizes([300, 900])

    def write(self, message):
        self.log.appendPlainText(message)

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

        self.write("Opened " + path.name)

    def save(self):

        if self.current:

            self.current.write_text(
                self.editor.toPlainText(),
                encoding="utf8",
            )

            self.write("Saved " + self.current.name)

    def new_post(self):

        if not self.project:
            return

        title, ok = QInputDialog.getText(
            self,
            "New Post",
            "Post title",
        )

        if not ok or not title:
            return

        slug = title.lower().replace(" ", "-")

        posts = self.project / "content" / "posts"
        posts.mkdir(
            parents=True,
            exist_ok=True,
        )

        file = posts / f"{slug}.md"

        file.write_text(
            f'''---
title: "{title}"
date: {datetime.date.today()}
tags: []
draft: false
---

# {title}

''',
            encoding="utf8",
        )

        self.model.setRootPath("")
        index = self.model.setRootPath(str(self.project))
        self.tree.setRootIndex(index)

        self.write("Created " + file.name)

    def preview(self):
        self.hugo.preview(self.project)

    def build(self):
        self.hugo.build(self.project)

    def md_help(self):
        show_markdown_help(self)