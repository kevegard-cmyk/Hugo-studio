Hugo Studio – The easiest way to start with Hugo.

Create, edit, preview and publish Hugo websites without learning the command line.

=======
VISION
=======

Hugo Studio is a desktop application that makes Hugo accessible to
beginners – writers, bloggers and other non-technical users.

Principles
----------
- Hide unnecessary complexity.
- Teach Hugo instead of exposing Hugo.
- Make common tasks one click.
- Keep generated projects 100% standard Hugo.
- Advanced users can still use the command line.


=================
CURRENT MILESTONE
=================

Architecture
- Split MainWindow
- Refactor project loading
- Split OS-specific code


=====
BUGS
=====

- Rename during open
- Remove during open
- Open only valid Hugo projects
- Text editor opens images (only open supported files)
- Delete message about missing project (or move after opening)
- QFileSystemWatcher warning after deleting directories
- PyInstaller doesn't include help file


========
FEATURES
========

IDE
---

Project
- Clear button for Recent Projects

Editor
- Extend editor toolbar
- Create Save/Save as button


Explorer
- Add folder icons
- Copy / Paste / Duplicate
- Copy path + filename
- Create more file types
- Extend Ctrl / Shift selection
- Remove file type column

Interface
- Window title information
- Remove status bar information
- Restructure menus


Hugo
-----

Create Site
- Improve New Project Wizard
- Theme installation
- Install theme from URL
- Fix theme .git installation issue

Configure Site
- Theme settings


Create Content
- Create Post Wizard

Build & Publish
- Preview settings
- Build settings
- Basic Git integration

Configure Site
- Config editor
- Menu editor
- Homepage editor


=========================
TOOLS & HELP & MAINTENANCE
=========================

Tools
-----
- YAML/TOML converter

Help
----
- Markdown Help formatting
- Hugo manual
- Git manual
- Hugo Studio manual

Maintenance
-----------
- Check Hugo/Git availability
- Check for updates


========
PROJECT
========

Website
- Create Hugo workflow
- Rewrite website content

GitHub
- Clean GitHub files


Release
--------
- Add release
- Make public


=========
FUTURE
=========

Hugo
- Site menu
- Theme manager
- Markdown highlighter

Other
- Additional improvements as the project evolves


=======
DONE
=======

- Multi-tab editor
- Ctrl+Z works with toolbar buttons
- Drag & Drop in Explorer
- Save automatically refreshes Preview
- Fixed save restoring deleted file
- Added Markdown Help