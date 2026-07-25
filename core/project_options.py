from dataclasses import dataclass
from pathlib import Path


@dataclass
class NewProjectOptions:
    parent_folder: Path
    name: str
    config_format: str
    initialize_git: bool