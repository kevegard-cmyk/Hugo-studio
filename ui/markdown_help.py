from PySide6.QtWidgets import QMessageBox


def show_markdown_help(parent):
    QMessageBox.information(
        parent,
        "Markdown Help",
        """# Heading
## Heading 2

**bold**
*italic*

- list
1. numbered

[Link](https://...)

![Image](image.png)

> Quote

```code```
"""
    )