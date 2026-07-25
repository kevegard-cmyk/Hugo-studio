from shutil import which


def check_installation():
    """Check whether Hugo and Git are available on the system."""

    return {
        "hugo": which("hugo") is not None,
        "git": which("git") is not None,
    }
    
