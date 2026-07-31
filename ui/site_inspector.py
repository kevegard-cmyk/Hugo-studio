from pathlib import Path


from PySide6.QtWidgets import (
    QMainWindow, 
    QWidget,
    QLabel,
    QVBoxLayout,
    QSplitter,
    QTreeView,
    QFileSystemModel,
)


class SiteInspector(QMainWindow):
    def __init__(self, project_path, parent=None):
        super().__init__(parent)

        self.project_path = Path(project_path)

        self.setWindowTitle("Site Inspector")
     
        
        central = QWidget()
        
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        splitter = QSplitter()

        layout.addWidget(splitter)
        
       
        # self.source_model.setRootPath(str(self.project_path))
        
        content_path = self.project_path / "content"

        self.source_model = QFileSystemModel()

        content_path = self.project_path / "content"
        self.source_model.setRootPath(str(content_path))

        self.source_tree = QTreeView()
        self.source_tree.setModel(self.source_model)
        self.source_tree.setRootIndex(
            self.source_model.index(str(content_path))
        )
        
        for i in range(1, self.source_model.columnCount()):
            self.source_tree.hideColumn(i)

        
        
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)

        left_layout.addWidget(QLabel("Source (content/)"))
        left_layout.addWidget(self.source_tree)

        splitter.addWidget(left_widget)
        
        public_path = self.project_path / "public"

        self.output_model = QFileSystemModel()
        self.output_model.setRootPath(str(public_path))
        
        

        self.output_tree = QTreeView()
        self.output_tree.setModel(self.output_model)
        self.output_tree.setRootIndex(
            self.output_model.index(str(public_path))
        )
        
        for i in range(1, self.output_model.columnCount()):
            self.output_tree.hideColumn(i)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        right_layout.addWidget(QLabel("Generated Site (public/)"))
        right_layout.addWidget(self.output_tree)

        splitter.addWidget(right_widget)
        splitter.setSizes([600, 600])

        # label = QLabel(
            # f"Site Inspector\n\nProject:\n{self.project_path}"
        # )
        # label.setAlignment(Qt.AlignCenter)

        # self.setCentralWidget(label)