import json
from pathlib import Path


SETTINGS_FILE = Path.home() / ".hugostudio.json"


DEFAULT_SETTINGS = {
    "last_project": "",
    "recent_projects": [],
    "editor_font_size": 11,
}


class Settings:

    def __init__(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):

        if not SETTINGS_FILE.exists():
            return

        try:
            self.settings.update(
                json.loads(
                    SETTINGS_FILE.read_text(
                        encoding="utf-8"
                    )
                )
            )

        except (json.JSONDecodeError, OSError):
            # Ignore invalid or unreadable settings.
            # Defaults will be used instead.
            pass

    def save(self):

        try:
            SETTINGS_FILE.write_text(
                json.dumps(
                    self.settings,
                    indent=4,
                ),
                encoding="utf-8",
            )

        except OSError:
            pass

    @property
    def last_project(self):
        return self.settings["last_project"]

    @last_project.setter
    def last_project(self, value):
        self.settings["last_project"] = value

    @property
    def recent_projects(self):
        return self.settings["recent_projects"]

    def add_recent_project(self, folder):
        
        folder = str(Path(folder).resolve())
        recent = self.settings["recent_projects"]

        if folder in recent:
            recent.remove(folder)

        recent.insert(0, folder)

        self.settings["recent_projects"] = recent[:10]
        
    @property
    def editor_font_size(self):
        return self.settings["editor_font_size"]


    @editor_font_size.setter
    def editor_font_size(self, value):
        self.settings["editor_font_size"] = value