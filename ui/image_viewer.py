from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGraphicsScene,
    QGraphicsView,
    QGraphicsPixmapItem,
    QLabel,
)


class ImageViewer(QDialog):
    def __init__(self, image_path, parent=None):
        super().__init__(parent)

        self.image_path = image_path

        self.setWindowTitle(image_path.name)
        self.resize(900, 700)

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Graphics view
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setFrameShape(QGraphicsView.NoFrame)
        layout.addWidget(self.view)

        # Status bar
        self.status = QLabel()
        self.status.setContentsMargins(8, 4, 8, 4)
        self.status.setStyleSheet("""
            QLabel {
                border-top: 1px solid palette(mid);
            }
        """)
        layout.addWidget(self.status)

        # Load image
        pixmap = QPixmap(str(image_path))

        if pixmap.isNull():
            self.status.setText(f"Unable to load '{image_path.name}'")
            return

        self.item = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.item)
        self.view.fitInView(self.item, Qt.KeepAspectRatio)

        # Status information
        size = image_path.stat().st_size
        size_mb = size / (1024 * 1024)

        self.status.setText(
            f"{image_path.name}    {pixmap.width()} × {pixmap.height()}    {size_mb:.1f} MB"
        )
            
     
            
    # def resizeEvent(self, event):
        # super().resizeEvent(event)

        # if hasattr(self, "item"):
            # self.view.fitInView(self.item, Qt.KeepAspectRatio)