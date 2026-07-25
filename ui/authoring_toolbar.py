from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QToolButton,
    QFrame,
)

from PySide6.QtCore import Qt
from PySide6.QtCore import QSize

from ui.icon import icon

MARKDOWN_BUTTONS = (
    "bold",
    "italic",
    "code",
    "strike",
    "h1",
    "h2",
    "h3",
    "bullet_list",
    "numbered_list",
    "quote",
)

class AuthoringToolbar(QWidget):

    def __init__(self, actions, save_action, save_as_action):
        super().__init__()
        
        self.buttons = {}

        self.layout = QHBoxLayout(self)

        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(3)
        
        self.add_action_button("save", save_action)
        self.add_action_button("save_as", save_as_action)
        self.add_separator()
        
        buttons = [
            ("bold", actions.bold, "Bold", "bold"),
            ("italic", actions.italic, "Italic", "italic"),
            ("code", actions.inline_code, "Inline code", "code"),
            ("strike", actions.strike, "Strikethrough", "strikethrough"),
            None,
            ("h1", actions.h1, "Heading 1", "heading-1"),
            ("h2", actions.h2, "Heading 2", "heading-2"),
            ("h3", actions.h3, "Heading 3", "heading-3"),
            None,
            ("bullet_list", actions.bullet_list, "Bullet list", "list"),
            ("numbered_list", actions.numbered_list, "Numbered list", "list-ordered"),
            ("quote", actions.quote, "Quote", "quote"),
        ]

        for item in buttons:
            if item is None:
                self.add_separator()
                continue

            key, slot, tooltip, icon_name = item

            self.add_button(
                key,
                slot,
                tooltip=tooltip,
                icon_name=icon_name,
            )

        self.layout.addStretch()

        
    def create_tool_button(self):
        button = QToolButton()
        button.setFixedSize(32, 28)
        button.setIconSize(QSize(22, 22))
        button.setToolButtonStyle(Qt.ToolButtonIconOnly)
        button.setAutoRaise(True)
        button.setCursor(Qt.PointingHandCursor)
        button.setFocusPolicy(Qt.NoFocus)
        return button
        
    def add_action_button(self, key, action):
        button = self.create_tool_button()
        button.setDefaultAction(action)

        self.layout.addWidget(button)
        self.buttons[key] = button
        return button
       
    def add_button(self, key, slot, tooltip, icon_name):
        button = self.create_tool_button()
        button.setIcon(icon(icon_name))
        button.setToolTip(tooltip)
        button.clicked.connect(slot)

        self.layout.addWidget(button)
        self.buttons[key] = button
        return button

    def add_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.VLine)
        line.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(line)
        
    def set_button_text(self, key, text):
        self.buttons[key].setText(text)
        
    def set_markdown_enabled(self, enabled: bool):
        for key in MARKDOWN_BUTTONS:
            self.buttons[key].setEnabled(enabled)