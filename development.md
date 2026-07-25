Hugo Studio – The easiest way to start with Hugo.

Create, edit, preview and publish Hugo websites without learning the command line.


VISION
======


Hugo Studio is a desktop application that makes Hugo accessible to
beginners – writers, bloggers and other non-technical users.

Principles
----------
- Hide unnecessary complexity.
- Teach Hugo instead of exposing Hugo.
- Make common tasks one click.
- Keep generated projects 100% standard Hugo.
- Advanced users can still use the command line.



CURRENT MILESTONE
======


Architecture
- Split MainWindow
- Refactor project loading
- Split OS-specific code



BUGS
======
- QFileSystemWatcher warning after deleting directories
- PyInstaller doesn't include help file



FEATURES
======


IDE
---

Project



Editor
- Extend editor toolbar with editor features (copy, paste,ctrl+z ctrl+y,)
- Extend editor toolbar with markdown features
- Extend editor toolbar with hugo features
- Implement toolbar enable/disable based on the active editor
- adding keyboard shortcuts to tooltips,


Explorer
- Add folder icons (?)
- Hide some directories or group them?
- Copy / Paste / Duplicate
- Copy path + filename
- Insert more file types
- Extend Ctrl / Shift selection
- Add file/folder info button
- Drag & Drop in Explorer (removed)

Interface
- Restructure menus


Hugo
-----

Create Site




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



TOOLS & HELP & MAINTENANCE
======


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



PROJECT
======


Website
- Create Hugo workflow
- Rewrite website content

GitHub
- Clean GitHub files


Release
--------
- Clear settings before release!




FUTURE
======


Hugo
- Site menu
- Theme manager
- Markdown highlighter

Other
- Additional improvements as the project evolves


DONE
======
- ZIP and clone theme installation
- Added menu to create more file types
- Improved New Project Wizard
- Added Close project menu
- Validate Hugo project before opening
- Added "Insert image function" to tree
- Added image viewer
- Toolbar reorganized, added icons
- Toolbar pointing hand cursor
- Only Folder and file names are shown in exlorer
- Files in explorer open only on double click
- Added Save/Save as button to editor
- Added "No project open text"
- Added project history clean button
- Added project name to windows title
- Editor only opens supported files
- Cannot rename or delete open file
- Multi-tab editor
- Ctrl+Z works with toolbar buttons
- Save automatically refreshes Preview
- Fixed save restoring deleted file
- Added Markdown Help