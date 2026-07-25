from pathlib import Path


ROOT_CONFIG_FILES = (
    "hugo.toml",
    "hugo.yaml",
    "hugo.yml",
    "hugo.json",
    "config.toml",
    "config.yaml",
    "config.yml",
    "config.json",
)

CONFIG_SUFFIXES = {".toml", ".yaml", ".yml", ".json"}


def validate_hugo_project(folder):
    """Return whether *folder* has a recognizable Hugo configuration."""
    project = Path(folder)

    if not project.is_dir():
        return False, "The selected folder does not exist."

    if any((project / name).is_file() for name in ROOT_CONFIG_FILES):
        return True, ""

    config_directory = project / "config"
    if config_directory.is_dir() and any(
        path.is_file() and path.suffix.lower() in CONFIG_SUFFIXES
        for path in config_directory.rglob("*")
    ):
        return True, ""

    return (
        False,
        "No Hugo configuration was found. Expected a hugo.toml, "
        "hugo.yaml, hugo.yml, hugo.json, or a populated config folder.",
    )
