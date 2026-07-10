from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
)


class AuthoringToolbar(QWidget):

    def __init__(self, actions):
        super().__init__()

        self.layout = QHBoxLayout(self)

        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(3)

        self.add_button("B", actions.bold)
        self.add_button("I", actions.italic)
        self.add_button("</>", actions.inline_code)
        self.add_button("S", actions.strike)

        self.add_separator()

        self.add_button("H1", actions.h1)
        self.add_button("H2", actions.h2)
        self.add_button("H3", actions.h3)

        self.add_separator()

        self.add_button("•", actions.bullet_list)
        self.add_button("1.", actions.numbered_list)
        self.add_button("❝", actions.quote)

        self.layout.addStretch()

    def add_button(self, text, slot):

        button = QPushButton(text)
        button.setFixedSize(32, 28)

        self.layout.addWidget(button)

        button.clicked.connect(slot)

        return button

    def add_separator(self):

        self.layout.addSpacing(8)