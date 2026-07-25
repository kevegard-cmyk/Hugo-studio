from pathlib import Path

from PySide6.QtGui import QIcon

ICON_DIR = (
    Path(__file__).resolve().parent.parent
    / "resources"
    / "icons"
    / "ui"
)

def icon(name: str) -> QIcon:
    return QIcon(str(ICON_DIR / f"{name}.svg"))