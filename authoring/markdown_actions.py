from PySide6.QtGui import QTextCursor


class MarkdownActions:

    def __init__(self, get_editor):
        self.get_editor = get_editor



  
        
    def bold(self):
        self.wrap_selection("**")

    def italic(self):
        self.wrap_selection("*")

    def inline_code(self):
        self.wrap_selection("`")

    def strike(self):
        self.wrap_selection("~~")
        
    
        
        
        
    def heading(self, level):
        self.prefix_lines("#" * level + " ")

    def h1(self):
        self.heading(1)

    def h2(self):
        self.heading(2)

    def h3(self):
        self.heading(3)
        
        
        
        
        
    def quote(self):
        self.prefix_lines("> ")

    def bullet_list(self):
        self.prefix_lines("- ")

    def numbered_list(self):
        self.prefix_lines("1. ")
        
        
        
        
        
        
    def wrap_selection(self, left, right=None):

        editor = self.get_editor()
        if editor is None:
            return

        if right is None:
            right = left

        cursor = editor.textCursor()
        cursor.beginEditBlock()

        text = cursor.selectedText()

        if text:
            cursor.insertText(f"{left}{text}{right}")
        else:
            cursor.insertText(f"{left}{right}")
            cursor.movePosition(
                QTextCursor.Left,
                QTextCursor.MoveAnchor,
                len(right)
            )

        cursor.endEditBlock()

        editor.setTextCursor(cursor)
        editor.setFocus()
        
    
    def prefix_lines(self, prefix):

        editor = self.get_editor()
        if editor is None:
            return

        cursor = editor.textCursor()

        cursor.beginEditBlock()

        if cursor.hasSelection():

            start = cursor.selectionStart()
            end = cursor.selectionEnd()

            cursor.setPosition(start)

            while True:

                cursor.movePosition(QTextCursor.StartOfLine)
                cursor.insertText(prefix)

                if cursor.position() >= end + len(prefix):
                    break

                if not cursor.movePosition(QTextCursor.Down):
                    break

        else:

            cursor.movePosition(QTextCursor.StartOfLine)
            cursor.insertText(prefix)

        cursor.endEditBlock()

        editor.setTextCursor(cursor)
        editor.setFocus()
        
    
        

        
    def insert_text(self, text):

        editor = self.get_editor()
        if editor is None:
            return

        cursor = editor.textCursor()

        cursor.beginEditBlock()
        cursor.insertText(text)
        cursor.endEditBlock()

        editor.setTextCursor(cursor)
        editor.setFocus()
        
    def insert_block(self, text):

        editor = self.get_editor()
        if editor is None:
            return

        cursor = editor.textCursor()

        cursor.beginEditBlock()
        cursor.insertText("\n" + text + "\n")
        cursor.endEditBlock()

        editor.setTextCursor(cursor)
        editor.setFocus()
        
    def selected_text(self):

        editor = self.get_editor()
        if editor is None:
            return ""

        return editor.textCursor().selectedText()