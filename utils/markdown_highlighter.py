from PySide6.QtGui import (
    QColor,
    QTextCharFormat,
    QFont,
    QSyntaxHighlighter,
)


class MarkdownHighlighter(QSyntaxHighlighter):
    """
    Lightweight Markdown syntax highlighter.

    Currently highlights:

    - Headings
    - Block quotes
    - Bold text
    """

    def __init__(self, document):
        super().__init__(document)

        self.heading_format = QTextCharFormat()
        self.heading_format.setForeground(QColor("blue"))
        self.heading_format.setFontWeight(QFont.Bold)

        self.bold_format = QTextCharFormat()
        self.bold_format.setForeground(QColor("darkGreen"))

        self.quote_format = QTextCharFormat()
        self.quote_format.setForeground(QColor("gray"))

    def highlightBlock(self, text: str):

        if text.startswith("#"):
            self.setFormat(
                0,
                len(text),
                self.heading_format,
            )

        if text.strip().startswith(">"):
            self.setFormat(
                0,
                len(text),
                self.quote_format,
            )

        start = text.find("**")

        while start != -1:

            end = text.find("**", start + 2)

            if end == -1:
                break

            self.setFormat(
                start,
                end - start + 2,
                self.bold_format,
            )

            start = text.find("**", end + 2)