

from PySide6.QtGui import QAction


def build_menus(window):

    menu = window.menuBar()

    build_file_menu(window, menu)
    build_view_menu(window, menu)
    build_hugo_menu(window, menu)
    build_theme_menu(window, menu)
    build_help_menu(window, menu)


def build_file_menu(window, menu):

    file_menu = menu.addMenu("&File")

    new_project = QAction("New Project...", window)
    new_project.triggered.connect(window.new_project)
    file_menu.addAction(new_project)

    open_action = QAction("Open Project...", window)
    open_action.triggered.connect(window.open_project)
    file_menu.addAction(open_action)

    window.recent_menu = file_menu.addMenu("Recent Projects")

    file_menu.addSeparator()

    window.save_action = file_menu.addAction("Save")
    window.save_action.setShortcut("Ctrl+S")
    window.save_action.triggered.connect(window.save)
    window.save_action.setEnabled(False)

    exit_action = QAction("Exit", window)
    exit_action.triggered.connect(window.close)
    file_menu.addAction(exit_action)


def build_view_menu(window, menu):

    view_menu = menu.addMenu("&View")

    font_up = QAction("Increase Font Size", window)
    font_up.setShortcut("Ctrl++")
    font_up.triggered.connect(window.increase_font_size)
    view_menu.addAction(font_up)

    font_down = QAction("Decrease Font Size", window)
    font_down.setShortcut("Ctrl+-")
    font_down.triggered.connect(window.decrease_font_size)
    view_menu.addAction(font_down)

    font_reset = QAction("Reset Font Size", window)
    font_reset.setShortcut("Ctrl+0")
    font_reset.triggered.connect(window.reset_font_size)
    view_menu.addAction(font_reset)


def build_hugo_menu(window, menu):

    hugo_menu = menu.addMenu("&Hugo")

    preview_action = QAction("Preview", window)
    preview_action.setShortcut("F5")
    preview_action.triggered.connect(window.preview)
    hugo_menu.addAction(preview_action)

    build_action = QAction("Build", window)
    build_action.setShortcut("F6")
    build_action.triggered.connect(window.build)
    hugo_menu.addAction(build_action)

    hugo_menu.addSeparator()


def build_theme_menu(window, menu):

    theme_menu = menu.addMenu("&Theme")

    install_theme_action = QAction("Install Theme...", window)
    install_theme_action.triggered.connect(window.install_theme)
    theme_menu.addAction(install_theme_action)


def build_help_menu(window, menu):

    help_menu = menu.addMenu("&Help")

    help_action = QAction("Markdown Help", window)
    help_action.setShortcut("F1")
    help_action.triggered.connect(window.md_help)
    help_menu.addAction(help_action)