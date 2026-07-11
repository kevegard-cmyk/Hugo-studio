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
        self.data = DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):

        if SETTINGS_FILE.exists():

            self.data.update(
                json.loads(
                    SETTINGS_FILE.read_text(
                        encoding="utf8"
                    )
                )
            )

    def save(self):

        SETTINGS_FILE.write_text(
            json.dumps(
                self.data,
                indent=4,
            ),
            encoding="utf8",
        )

    @property
    def last_project(self):
        return self.data["last_project"]

    @last_project.setter
    def last_project(self, value):
        self.data["last_project"] = value

    @property
    def recent_projects(self):
        return self.data["recent_projects"]

    def add_recent_project(self, folder):
        
        folder = str(Path(folder).resolve())
        recent = self.data["recent_projects"]

        if folder in recent:
            recent.remove(folder)

        recent.insert(0, folder)

        self.data["recent_projects"] = recent[:10]
        
    @property
    def editor_font_size(self):
        return self.data["editor_font_size"]


    @editor_font_size.setter
    def editor_font_size(self, value):
        self.data["editor_font_size"] = value