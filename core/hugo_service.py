import subprocess
import webbrowser

from PySide6.QtCore import QProcess, QTimer


class HugoService:
    def __init__(self, parent):
        self.parent = parent
        self.process = QProcess(parent)

    def preview(self, project):

        if project is None:
            return

        if self.process.state() == QProcess.NotRunning:

            self.process.setWorkingDirectory(str(project))
            self.process.start(
                "hugo",
                [
                    "server",
                    "--disableFastRender",
                ],
            )

            self.parent.write("Starting Hugo server...")

            QTimer.singleShot(
                2500,
                lambda: webbrowser.open("http://localhost:1313"),
            )

        else:

            webbrowser.open("http://localhost:1313")
            self.parent.write("Opened browser.")

    def build(self, project):

        if project is None:
            return

        subprocess.run(
            ["hugo"],
            cwd=project,
        )

        self.parent.write("Build complete.")