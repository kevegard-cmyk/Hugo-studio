import json
from pathlib import Path


SETTINGS_FILE = Path.home() / ".myhugodesk" / "settings.json"


DEFAULT_SETTINGS = {
    "last_project": "",
    "recent_projects": [],
    "editor_font_size": 11,

    "first_run": True,
    "hugo_available": False,
    "git_available": False,
}


class Settings:

    def __init__(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.load()

    def load(self):
        SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
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
            SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
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
        
        
    @property
    def first_run(self):
        return self.settings["first_run"]

    @first_run.setter
    def first_run(self, value):
        self.settings["first_run"] = value


    @property
    def hugo_available(self):
        return self.settings["hugo_available"]

    @hugo_available.setter
    def hugo_available(self, value):
        self.settings["hugo_available"] = value


    @property
    def git_available(self):
        return self.settings["git_available"]

    @git_available.setter
    def git_available(self, value):
        self.settings["git_available"] = value