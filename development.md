MyHugoDesk – The easiest way to start with Hugo.

Create, edit, preview and publish Hugo websites without  command line.


VISION
======


MyHugoDesk is a desktop application that makes Hugo accessible to
beginners.


Principles
----------
- Teach Hugo instead of exposing Hugo.
- Keep generated projects 100% standard Hugo.
- Advanced users can still use the command line.



CURRENT MILESTONE
======


Architecture
- Refactor project loading
- Split OS-specific code



BUGS, ISSUES
======
- Rename cannot fix case sensitivity
- Theme install dialog "git clone" without opened project - causes freezing 
- Site inspector right click open html without css
- What if two instances of the IDE are running at the same time?
- If there is no public folder, Siteinspector shows system root
- Terminal is visible but not functional
- Satus bar server state only visible after change, then disappears
- If clear recent projects when projects is open, it delete current project status

FEATURES to add
======

IDE
-----


UI Polish

- Progress indicators to dialogs


Editor
- Extend editor toolbar with editor features (copy, paste,ctrl+z ctrl+y,)
- Extend editor toolbar with markdown features
- Extend editor toolbar with hugo content features
- Implement toolbar enable/disable based on the active editor
- adding keyboard shortcuts and tooltips,
- search text


Explorer
- Add folder icons
- Copy / Paste / Duplicate
- Copy path + filename
- Insert more file types
- Extend Ctrl / Shift selection
- Add file/folder info button
- info for folders and files

Status bar


Hugo
-----

- Add stop preview (server) button 

Build & Publish
- Build settings
- Build output summary
- Improve two panel site inspector (content/public folders)
- Basic Git integration



TOOLS & HELP & MAINTENANCE to add
======

Tools
-----
- YAML/TOML converter
- Hugo and git install check

Help
----
- Markdown Help formatting
- Hugo manual
- Git manual
- MyHugoDesk manual

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



Release
--------


FUTURE
======




Hugo
--------
- Site menu
- Markdown highlighter
- YAML/TOML/JSON highlighters


Configure Site
--------
- Config editor
- Menu editor
- Homepage editor
- Theme manager, settings

Create Content
--------
- Create Post Wizard



Other
- Additional improvements as the project evolves
- Drag & Drop in Explorer (removed)
- Hide some directories or group them?

DONE
======
- Added preview settings dialog with stop server function and save settings
- Improved New project dialog, save settings
- Fixed theme install freeze
- Added 'site inspector'
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